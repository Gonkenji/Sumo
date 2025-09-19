import uasyncio as asyncio
import aioble
import bluetooth
import sys

HID_SERVICE_UUID = bluetooth.UUID(0x1812)
HID_INPUT_UUID = bluetooth.UUID(0x2A4D)
MAC_CONTROLE = "e4:17:d8:5a:41:94"

led2 = machine.Pin(28 , machine.Pin.OUT)
led_da_placa = machine.Pin('LED', machine.Pin.OUT)

led_da_placa.value(0)

mapeamento7 = {
'1': "A",
'2': "B",
'8': "X",
'16': "Y"}# Os botoes simples são dado[7]

mapeamento0 = {
'0': "Cima",
'2': "Direita",
'6': "Esquerda",
'4': "Baixo" # As setinhas sao dado[0]
} 

async def botoes(con, trab, car):
    dado_anterior = None
    async with con:
        print("Inscrevendo-se para notificações...")
        await car.subscribe(notify=True)
        print("Inscrição concluída. Aguardando dados do controle...")
        led_da_placa.value(1)
        while con.is_connected():
            # Espera até que uma notificação seja recebida do controle
            dado = await car.notified()
                
            if dado != dado_anterior:
                # A linha de print mais importante!
                print(f"Hex: {dado.hex(' ')}")
                dado_anterior = dado
                
                if (str(dado[7])) in mapeamento7:
                    print(mapeamento7[str(dado[7])])
                
                if (str(dado[0])) in mapeamento0:
                    print(mapeamento0[str(dado[0])])
                    
            await asyncio.sleep_ms(500)

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
