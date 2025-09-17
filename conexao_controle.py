import uasyncio as asyncio
import aioble

MAC_CONTROLE = "e4:17:d8:5a:41:94" #Mac específico do controle
    
async def conecta_ao_controle(mac):
    print("Iniciando a busca por dispositivos...")
    
    # Inicia o escaneamento
    async with aioble.scan(30000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for device in scanner:
            if str(device.device.addr_hex()) == mac:
                print("Conectando")
                controle = device.device
                await controle.connect()
                print("Conectado")
                
# Inicia a execução do programa
asyncio.run(conecta_ao_controle(MAC_CONTROLE))
