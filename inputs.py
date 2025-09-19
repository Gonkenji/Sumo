import uasyncio as asyncio
import aioble
import bluetooth
import sys

HID_SERVICE_UUID = bluetooth.UUID(0x1812)
HID_INPUT_UUID = bluetooth.UUID(0x2A4D)
MAC_CONTROLE = "e4:17:d8:5a:41:94"

async def botoes(con, trab, car):    
    async with con:
        print("Inscrevendo-se para notificações...")
        await car.subscribe(notify=True)
        print("Inscrição concluída. Aguardando dados do controle...")

        while con.is_connected():
            # Espera até que uma notificação seja recebida do controle
            data = await car.notified()
            
            # 'data' é um bytearray com o estado dos botões e analógicos
            print(data)
            
            await asyncio.sleep_ms(1000)

async def conecta_ao_controle(mac):
    print("Iniciando a busca por dispositivos...")
    
    # Inicia o escaneamento
    async with aioble.scan(30000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for device in scanner:
            if str(device.device.addr_hex()) == mac:
                print("Conectando...")
                controle = device.device
                conexao = await controle.connect()
                print("Conectado")
                trabalho = None
                caracteristica = None
                
                while trabalho == None:
                    trabalho = await conexao.service(HID_SERVICE_UUID)
                    
                while caracteristica == None:
                    caracteristica = await trabalho.characteristic(HID_INPUT_UUID)
                
                asyncio.run(botoes(conexao, trabalho, caracteristica))
            
# Inicia a execução do programa
asyncio.run(conecta_ao_controle(MAC_CONTROLE))



