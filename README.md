# Biblioteca de Comunicação para Inversores de Frequência (`LCINVfunctions`)

-----

## Visão Geral

A biblioteca `LCINVfunctions` é um conjunto de módulos Python desenvolvido para facilitar a comunicação serial com inversores de frequência através de um protocolo baseado em telegramas de bytes. Esta biblioteca abstrai a construção de frames, a decomposição de parâmetros de 16 bits e o cálculo de redundância (BCC), permitindo o controle de velocidade e o ajuste de parâmetros de hardware de forma simplificada.

-----

## Contexto de Utilização no Projeto "Bancada de Emulação de Turbina Eólica Integrada em Microrrede"

No âmbito do projeto de pesquisa "BANCADA DE EMULAÇÃO DE TURBINA EÓLICA INTEGRADA EM MICRORREDE", a **biblioteca `LCINVfunctions`** desempenha o papel de atuador no sistema. Enquanto a biblioteca `LCTSfunctions` monitora o torque e o RPM, a `LCINVfunctions` é utilizada para enviar comandos de referência de velocidade e ajustar parâmetros operacionais do inversor.

Esta biblioteca viabiliza a **atuação em tempo real**, permitindo que o sistema de controle ajuste a dinâmica do motor para reproduzir fielmente o comportamento de uma turbina real sob diversas condições de vento. A confiabilidade e agilidade no envio de telegramas são fundamentais para a validação de algoritmos avançados de controle em ambiente de laboratório.

#### Configuração do Protocolo do Inversor
* **STX**: 0x02 (Início de texto).
* **ADR**: Endereço do inversor (P0308 + 64).
* **COD**: Leitura (0x3C) ou Escrita (0x3D).
* **NUM**: Quantidade de parâmetros lidos/escritos (Padrão: 1).
* **BCC**: Checksum Longitudinal calculado via OU EXCLUSIVO (XOR).

-----

## Fluxograma de Alto Nível do Processo de Comunicação

O processo de interação com o inversor através desta biblioteca segue o fluxo:

1.  **Inicialização**: Criação de uma instância da classe `Inverter` com porta serial e endereço (1 a 30).
2.  **Montagem do Telegrama**: O comando é estruturado com bytes de controle (STX, COD, NUM, ETX) e decomposição do parâmetro em bytes HI e LO.
3.  **Cálculo de BCC**: Aplicação de lógica XOR em todos os bytes do corpo da mensagem.
4.  **Transmissão**: Envio do telegrama via porta serial utilizando a biblioteca `pyserial`.
5.  **Aguardando Resposta**: Monitoramento do retorno para extrair dados (Leitura) ou confirmar recebimento (Escrita).
6.  **Verificação e Conversão**: Verificação da integridade via BCC e conversão dos bytes recebidos para valor inteiro.

-----

## Formato do Telegrama

Os telegramas seguem o formato padrão de bytes:

  * **`STX` (0x02)**: Início do telegrama.
  * **`ADR`**: Endereço do dispositivo na rede.
  * **`COD`**: Operação (0x3C para leitura, 0x3D para escrita).
  * **`NUM`**: Número de parâmetros operados.
  * **`DMR / DMW`**: Parâmetro lido ou escrito (incluindo valores em caso de escrita).
  * **`ETX` (0x03)**: Fim do texto.
  * **`BCC`**: Byte de verificação por XOR.

-----

## Comandos Disponíveis

A biblioteca implementa as seguintes constantes e operações:

  * `STX = 0x02`
  * `ETX = 0x03`
  * `COD_READ = 0x3C`
  * `COD_WRITE = 0x3D`

-----

## Instalação

Para utilizar esta biblioteca, você precisará do Python e da biblioteca `pyserial` instalados.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/LCINVfunctions.git](https://github.com/seu-usuario/LCINVfunctions.git)
    cd LCINVfunctions
    ```
2.  **Instale as dependências:**
    ```bash
    pip install pyserial
    ```

-----

## Como Usar

### `Inverter` Classe

Esta classe gerencia a interface de comunicação e operações de baixo nível com o inversor.

#### `__init__(self, Port: str, ADR=1, Baudrate=9600, Timeout=0.05)`

Inicializa a comunicação com o inversor.

  * `Port` (str): Nome da porta serial (ex: 'COM1' ou '/dev/ttyUSB0').
  * `ADR` (int): Endereço do inversor (1 a 30).
  * `Baudrate` (int): Velocidade de transmissão (Padrão: 9600).
  * `Timeout` (float): Tempo de espera para dados (Padrão: 0.05s).

#### Métodos Principais

  * **`ReadParameter(parameter: int, tries=1)`**: Lê o valor de um parâmetro do inversor.
      * `parameter` (int): Número do parâmetro (ex: 2 para P0002).
      * Retorna: `int` (valor lido) ou `None`.
  * **`WriteParameter(parameter: int, value: int, tries=1)`**: Escreve um valor em um parâmetro específico.
      * `parameter` (int): Número do parâmetro.
      * `value` (int): Valor a ser configurado.
      * Retorna: `bool` (True para sucesso na escrita).
  * **`SendReferenceAngularVelocity(referencia_rpm)`**: Converte RPM para a escala do inversor e envia para o parâmetro 683.

### Exemplo de Uso (Básico)

```python
from LCINVfunctions import Inverter

# Configurações do sistema
PORTA_SERIAL = 'COM4'
ADR_INVERSOR = 1

try:
    # Inicializa o objeto do Inversor
    inversor = Inverter(Port=PORTA_SERIAL, ADR=ADR_INVERSOR)
    print(f"Inversor conectado na porta {PORTA_SERIAL}.")

    # Exemplo: Ler valor de um parâmetro (Ex: P0002)
    valor = inversor.ReadParameter(2)
    if valor is not None:
        print(f"Valor do Parâmetro P0002: {valor}")

    # Exemplo: Enviar referência de velocidade (RPM)
    # Internamente envia o valor convertido para o parâmetro 683
    sucesso = inversor.SendReferenceAngularVelocity(1500)
    if sucesso:
        print("Velocidade de 1500 RPM enviada com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
