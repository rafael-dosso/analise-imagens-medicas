# Análise de Imagens Médicas no Formato DICOM

## Descrição

Este projeto foi desenvolvido como parte de um processo seletivo, buscando simular interações com sistemas reais de ambiente hospitalar, incluindo o uso de PACS e arquivos DICOM.

O objetivo principal foi configurar um sistema PACS OrthanC, manipular arquivos DICOM, realizar a classificação de achados utilizando um modelo pré-treinado, e criar e enviar relatórios estruturados DICOM (DICOM SR) para o PACS.

## Índice

1. [Instalação e Execução](#instalação-e-execução)
2. [Desafios e Soluções](#desafios-e-soluções)
3. [Considerações Finais](#considerações-finais)

## Instalação e execução

### Requisitos

- Docker
- Python 3.x

### Passos para instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/rafael-dosso/projeto-miclab.git
   ```
2. **Navegue até o diretório do projeto**:

   ```bash
    cd projeto-miclab
   ```

#### Execução via Docker

3. **Construa a imagem Docker da aplicação**:
   ```bash
    sudo docker build -t rafael-dosso-miclab .
   ```
   Este passo pode demorar um pouco, pois as instalações do TorchXRayVision são extensas.
4. **Execute o contêiner composto da aplicação e do PACs Orthanc**:
   ```bash
    sudo docker compose up --build
   ```

O visualizador web do Orthanc já estará acessível no endereço [localhost:8042](http://localhost:8042) após a execução do Docker Compose, e, em seguida, você poderá acompanhar o envio dos arquivos pelos logs da aplicação Python. Se for pedida alguma autenticação no PACs, o usuário e senha são ambos "orthanc".

5. **Após o uso, termine a aplicação:**
   ```bash
    sudo docker compose down
   ```

#### Execução local

Para executar o programa localmente, você deve executar a API do Orthanc na sua máquina. Nesse caso, é necessário descomentar a linha 11 do arquivo `send_dicom.py` e comentar a linha 12. Isso fará com que as requisições sejam mandadas para o localhost em vez dos endereços definidos internamente pelo Docker, garantindo o funcionamento da aplicação.

3. **Certifique-se de que está rodando o PACs Orthanc localmente. Se não estiver, você pode usar a imagem [jodogne/orthanc](https://orthanc.uclouvain.be/book/users/docker.html):**
   ```bash
    sudo docker pull jodogne/orthanc
    sudo docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc
   ```
4. **Instale as dependências do python:**
   ```bash
    pip install -r requirements.txt
   ```
5. **Execute o código da main:**
   ```bash
    python3 src/main.py
   ```

## Desafios e Soluções

### Configuração e Execução do PACS Orthanc

Inicialmente, eu não tinha experiência com Docker. Após alguns estudos e consultas, consegui fazer a instalação e entender os seus conceitos básicos. Encontrei a imagem oficial do Orthanc (`jodogne/orthanc`), e, seguindo o passo a passo da documentação, não tive problemas em executá-la e ter acesso à API localmente.

### Envio de Arquivos DICOM

Assistentes virtuais como o ChatGPT e o Perplexity.AI me deram uma noção do funcionamento do PACs Orthanc, e a partir daí elaborei um script que envia os arquivos DICOM para a API REST. Comecei utilizando a biblioteca `requests` do Python, mas percebi que o corpo das requisições não estava sendo recebido. Este erro persistia somente em Python. Com o Curl, por exemplo, isto não ocorria, o que me indicou que talvez fosse um problema com a biblioteca. Após algumas pesquisas, encontrei [uma implementação](https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.12.4/OrthancServer/Resources/Samples/ImportDicomFiles/ImportDicomFiles.py) de requisições HTTP feita pela própria organização que mantém o Orthanc, e me baseei nela para resolver o problema que tivera.

### Análise de Imagens DICOM com TorchXRayVision

Para essa implementação, me baseei na seção Get Started da documentação oficial da biblioteca. Substituí a linha `img = skimage.io.imread()` pela função `xrv.utils.read_xray_dcm`, o que gerou exceções no tratamento da imagem. Após analisar os logs, verifiquei que o vetor de pixels da imagem DICOM não tinha as dimensões que a biblioteca esperava, e resolvi isso adicionando mais um eixo ao tensor.
Além disso, em algumas imagens, obtive a exceção `max image value (8191) higher than expected bound (4095)`. Foi difícil encontrar documentações que explicassem melhor o que estava acontencendo, e, além disso, as informações do ChatGPT estavam obsoletas devido ao seu treinamento datado. Nesse caso, o Perplexity.AI foi muito útil para me orientar, pois seu treinamento está sempre atualizado. A solução para este problema foi perceber que o padrão da biblioteca é esperar valores de 12 bits nos pixels, o que não era o caso com os arquivos DICOM fornecidos. Pensando nisso, normalizei o vetor de pixels para um máximo de 4095 quando isso ocorria, enquadrando os valores intervalo.

### Geração e Envio de DICOM SR

Desenvolvi uma função para criar o DICOM SR com base nas informações das imagens e resultados do modelo. A falta de documentações e exemplos de SRs na internet foi um obstáculo. Foi difícil entender como se estruturava esse tipo de arquivo, ainda mais quando tinha que montá-lo do zero em Python. Mais uma vez, o Perplexity.AI me forneceu um panorama sobre o formato destes relatórios, e, aos poucos, foi possível montá-los. A estruturação dos dados me pareceu um pouco confusa, já que não encontrei um padrão definido sobre como expor pares de chave-valor nessa arquitetura, mas busquei a maneira que me pareceu mais clara para os implementar.

### Geração de Dockerfile

Após criar o Dockerfile para a aplicação Python e inserir as informações relevantes nele, tentei executá-lo, mas o script não estava conseguindo acessar a API do Orthanc. O motivo disso é que o URL usado referenciava o `localhost`, e provavelmente o localhost interno do contêiner não aponta para o mesmo endereço da minha máquina. Nesse contexto, considerei utilizar o IP estático da minha máquina, mas o problema disso era a impossibilidade de execução da imagem em outra máquina. A próxima ideia foi utilizar `host.docker.internal`, o que referencia o endereço de quem está hosteando o contêiner. Essa solução também era inviável, já que não pode ser utilizada em sistemas operacionais Linux.
A solução que encontrei foi o uso do Docker Compose, que permite relacionar contêineres e executá-los simultaneamente como um único aplicativo. Nesse caso, foi possível iniciar a imagem do Orthanc juntamente com a da aplicação, e aplicar um apelido para o seu endereço. Assim, este apelido pode ser referenciado no código Python e o acesso à API é possível.

## Considerações Finais

Durante o desenvolvimento, foi necessário ajustar várias etapas do processo para lidar com as especificidades das ferramentas. A manipulação dos valores de pixels e a adaptação dos dados ao formato esperado pelo modelo foram cruciais para garantir a precisão na análise das imagens. Além disso, a escassez de documentações disponíveis foi um obstáculo constante, mas isso me levou a buscar soluções de forma autônoma e proativa. Mesmo com as dificuldades, as soluções implementadas garantiram o sucesso do projeto.
