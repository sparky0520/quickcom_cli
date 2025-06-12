from helpers import *
from platforms.instamart import fetch_swiggy_prices
from platforms.blinkit import fetch_blinkit_prices
from platforms.zepto import fetch_zepto_prices

import asyncio

async def main():
    query = input("Enter the product you want to search: ")
    
    pretty_print(text="QuickCom",font="slant" )

    print("\n\nFetching Blinkit...")
    blinkit = await fetch_blinkit_prices(query)
    save_to_file(blinkit, "__blinkit_prices", "csv")
    print("Blinkit Results generated! Please checkout the file created.")

    print("\n\nFetching Swiggy...")
    swiggy = await fetch_swiggy_prices(query)
    save_to_file(swiggy, "__swiggy_prices", "csv")
    print("Swiggy Results generated! Please checkout the file created.")

    print("\n\nFetching Zepto...")
    zepto = await fetch_zepto_prices(query)
    save_to_file(zepto, "__zepto_prices", "csv")
    print("Zepto Results generated! Please checkout the file created.")

if __name__ == "__main__":
    asyncio.run(main())
