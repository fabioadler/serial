from construct import Struct, Byte, Int16ub, Padding, GreedyBytes
import serial.tools.list_ports as ls_ports
import serial,time,binascii

devices = ls_ports.comports()
devices_info = []
for c in devices:
    devices_info.append({"porta":c.name,"fabricante":c.manufacturer,"hwid":c.hwid,"pid":c.pid})

#def parse_message(data):
#    """
#    Exemplo fictício para demonstrar a conversão de dados binários.
#    
#    Suponha que o protocolo seja:
#      - Byte 0: Início do Pacote (deve ser 0x01)
#      - Byte 1: Código do Comando
#      - Byte 2 a 3: Parâmetro (um inteiro de 2 bytes, big-endian)
#      - Byte 4 a -3: Payload (dados diversos)
#      - Byte -2: Checksum (por exemplo, soma módulo 256 dos dados)
#      - Byte -1: Fim do Pacote (por exemplo, \n)
#    """
#    
# Validação básica do tamanho da mensagem
#    if len(data) < 6:
#        return "Mensagem muito curta para ser válida"
#    
# Verifica se a mensagem inicia e termina com os bytes esperados
#    if data[0] != 0x01 or data[-1] != 0x0A:
#        return "Formato de mensagem inválido (cabeçalho ou rodapé não conferem)"
#    
# Extraindo os campos conforme nossa hipótese
#    cabecalho = data[0]
#    comando   = data[1]
#    parametro = struct.unpack('>H', data[2:4])[0]  # '>H' para unsigned short em big-endian
#    payload   = data[4:-2]
#    checksum  = data[-2]
#    
#    # Vamos supor um dicionário de mapeamento dos códigos de comando para texto
#    comandos_map = {
#        0x00: "NENHUM",
#        0x06: "INICIAR",
#        0x10: "PARAR",
# Adicione outros mapeamentos conforme o protocolo ...
#    }
#    
#    comando_texto = comandos_map.get(comando, f"Comando desconhecido (0x{comando:02X})")
#    
# Exemplo simples de verificação de checksum (soma dos bytes do payload modulo 256)
#    checksum_calculado = sum(payload) % 256
#    valid_checksum = (checksum_calculado == checksum)
#    
# Monta uma resposta legível
#    resposta = (
#        f"Pacote:\n"
#        f" - Cabeçalho: 0x{cabecalho:02X}\n"
#        f" - Comando: {comando_texto} (0x{comando:02X})\n"
#        f" - Parâmetro: {parametro}\n"
#        f" - Payload: {payload.hex()}\n"
#        f" - Checksum: 0x{checksum:02X} (calculado: 0x{checksum_calculado:02X}) {'OK' if valid_checksum else 'ERRO'}\n"
#        f" - Fim do Pacote: 0x{data[-1]:02X}"
#    )
#   
#    return resposta

mensagem = Struct(
    "cabeçalho" / Byte,
    "comando" / Byte,
    "valor" / Int16ub,
    "payload" / GreedyBytes  # Pega o restante dos bytes como payload
)

arq = open("log.txt","w",encoding="utf-8")
com = serial.Serial(devices_info[0]['porta'],baudrate=115200)
com.reset_input_buffer()
com.reset_output_buffer()
time.sleep(2)
while(True):
    dados = com.readline() 
    unhex_dados = binascii.unhexlify(binascii.hexlify(dados))
    utf_8_dados = dados.decode('utf-8',errors="replace").strip()
    #f_dados = parse_message(dados)

    if(dados != b""):
        arq.write(f"Dados bin: {unhex_dados}\n")
        arq.write(f"Dados utf-8: {utf_8_dados}\n")
        try:
            arq.write(f"{mensagem.parse(unhex_dados)}\n\n")
        except:
            arq.write(f"Erro ao parsear mensagem\n\n")
        #arq.write(f"{f_dados}\n")
        #f_dados_s = f_dados.split("\n")
        #if(len(f_dados_s)>=2):
        #   payload = (f_dados_s[len(f_dados_s)-3].split(":")[1]).strip()
        #    arq.write(f"conteudo da payload:\n")
        #    for i, byte in enumerate(payload, start=1):
        #        # Se o byte for imprimível (32 a 126), mostra o caractere; caso contrário, exibe '.'
        #        try:
        #            char = chr(byte)
        #        except:
        #            char = byte
        #        arq.write(f"Byte {i:2d}: 0x{byte} ({byte}) -> {char}\n")
        #    arq.write(f"Fim do conteudo da payload\n\n")
        #else:
        #    pass
    else:
        pass