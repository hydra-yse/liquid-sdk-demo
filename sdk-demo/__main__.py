import asyncio
import breez_sdk_liquid

from mnemonic import Mnemonic
from asyncio import AbstractEventLoop, Queue
from breez_sdk_liquid.breez_sdk_liquid import ConnectRequest, EventListener, LiquidNetwork, PaymentMethod, PrepareReceiveRequest, PrepareSendRequest, ReceivePaymentRequest, SdkEvent, SendPaymentRequest, connect, default_config

DATA_DIR = ".data"

class DemoListener(EventListener):
    loop: AbstractEventLoop
    receive_queue: Queue[str]

    def __init__(self, loop: AbstractEventLoop, receive_queue: Queue[str]) -> None:
        super().__init__()
        self.loop = loop
        self.receive_queue = receive_queue
    
    def on_event(self, e: SdkEvent):
        print(f"Received new event: {e}")
        if isinstance(e, SdkEvent.PAYMENT_SUCCEEDED) and e.details.tx_id is not None:
            asyncio.run_coroutine_threadsafe(self.receive_queue.put(e.details.tx_id), self.loop)

class DemoSDK():
    instance: breez_sdk_liquid.BindingLiquidSdk
    receive_queue: Queue[str]

    def get_mnemonic(self) -> str:
        """
        You can generate a new mnemonic by uncommenting the lines below. 
        Make sure to print it and return it here, or your funds will be gone!
        """
        # mnemonic = Mnemonic("english").generate(strength=256)
        # print(mnemonic)
        # return mnemonic
        return "TODO: INSERT MNEMONIC HERE"

    def __init__(self, data_dir: str):
        """
        Step 1: Define an `init` method which connects to the SDK
        NOTE: It is suggested to set `config.working_dir` to the global DATA_DIR variable
        """
        mnemonic = self.get_mnemonic()
        config = default_config(network=LiquidNetwork.TESTNET)
        config.working_dir = data_dir
        connect_request = ConnectRequest(config=config, mnemonic=mnemonic)
        self.instance = connect(req=connect_request)
        
        self.receive_queue = Queue()
        listener = DemoListener(asyncio.get_running_loop(), self.receive_queue)
        self.instance.add_event_listener(listener)
    
    def get_info(self) -> breez_sdk_liquid.GetInfoResponse: # type: ignore[reportReturnType]
        """Step 2: Retrieve the wallet's information"""
        return self.instance.get_info()

    def get_funding_address(self, amount_sat: int) -> str: # type: ignore[reportReturnType]
        """Step 3: Get an address so we can fund the wallet"""
        prepare_req = PrepareReceiveRequest(payer_amount_sat=amount_sat,payment_method=PaymentMethod.LIQUID_ADDRESS)
        prepare_response = self.instance.prepare_receive_payment(prepare_req)
        res = self.instance.receive_payment(ReceivePaymentRequest(prepare_response=prepare_response))
        return res.destination

    def send_payment(self, amount_sat: int, destination: str) -> breez_sdk_liquid.Payment: # type: ignore[reportReturnType]
        """Step 4: Send funds to a Liquid, Lightning or Bitcoin address"""
        prepare_req = PrepareSendRequest(amount_sat=amount_sat, destination=destination)
        prepare_response = self.instance.prepare_send_payment(prepare_req)
        res = self.instance.send_payment(SendPaymentRequest(prepare_response=prepare_response))
        return res.payment

    async def wait_for_payment(self):
        """
        Step 5: Use an Event Listener to wait for new payments
        NOTE: Make sure you add the event listener to the __init__ method!
        """
        txid = await self.receive_queue.get()
        print(f"Received new payment: txid {txid}")

async def main():
    sdk = DemoSDK(DATA_DIR)
    amount_sat = 1000
    destination = sdk.get_funding_address(amount_sat)
    print(f"Please pay {amount_sat} sat to destination: {destination}")
    await sdk.wait_for_payment()
    sdk.instance.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
