import breez_sdk_liquid
from mnemonic import Mnemonic

DATA_DIR = ".data"

class DemoSDK():
    instance: breez_sdk_liquid.BindingLiquidSdk

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

    
    def get_info(self) -> breez_sdk_liquid.GetInfoResponse: # type: ignore[reportReturnType]
        """Step 2: Retrieve the wallet's information"""

    def get_funding_address(self, amount_sat: int) -> str: # type: ignore[reportReturnType]
        """Step 3: Get an address so we can fund the wallet"""

    def send_payment(self, amount_sat: int, destination: str) -> breez_sdk_liquid.Payment: # type: ignore[reportReturnType]
        """Step 4: Send funds to a Liquid, Lightning or Bitcoin address"""

    async def wait_for_payment(self):
        """
        Step 4: Use an Event Listener to wait for new payments
        NOTE: Make sure you add the event listener to the __init__ method!
        """

if __name__ == "__main__":
    sdk = DemoSDK(DATA_DIR)

    """your commands go here..."""

    sdk.instance.disconnect()
