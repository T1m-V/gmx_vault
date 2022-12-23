import json

from web3 import HTTPProvider, Web3

from func_file_ut import open_file

# Connect to web3
api = open_file("input/private/api.txt")

w3 = Web3(
    HTTPProvider(f"https://soft-muddy-wildflower.arbitrum-mainnet.discover.quiknode.pro/{api}/")
)

# Read ABI from JSON files
with open("input/abi/abi_usdc.json") as f:
    abi_usdc = json.load(f)
with open("input/abi/abi_glp.json") as f:
    abi_glp = json.load(f)

# Adresses in the vault
gmx_vault_address_list = {
    "USDC": {"address": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8", "decimals": 6},
    "WETH": {"address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "decimals": 18},
    "WBTC": {"address": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f", "decimals": 8},
    "DAI": {"address": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1", "decimals": 18},
    "USDT": {"address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9", "decimals": 6},
    "FRAX": {"address": "0x17FC002b466eEc40DaE837Fc4bE5c67993ddBd6F", "decimals": 18},
    "LINK": {"address": "0xf97f4df75117a78c1A5a0DBb814Af92458539FB4", "decimals": 18},
    "UNI": {"address": "0xFa7F8980b0f1E64A2062791cc3b0871572f1F7f0", "decimals": 18},
}

# Define tokens
gmx_vault = "0x489ee077994B6658eAfA855C308275EAd8097C4A"
for token in gmx_vault_address_list:
    gmx_vault_address_list[token]["token"] = w3.eth.contract(
        address=gmx_vault_address_list[token]["address"], abi=abi_usdc
    )
    gmx_vault_address_list[token]["gmx_vault_supply_raw"] = (
        gmx_vault_address_list[token]["token"].functions.balanceOf(gmx_vault).call()
    )
    gmx_vault_address_list[token]["gmx_vault_supply"] = gmx_vault_address_list[token][
        "gmx_vault_supply_raw"
    ] / (10 ** gmx_vault_address_list[token]["decimals"])

# Calculate my percentage
address = open_file("input/private/private_address.txt")
address_glp = "0x4277f8F2c384827B5273592FF7CeBd9f2C1ac258"
address_fee_staked_glp = "0x1aDDD80E6039594eE970E5872D247bf0414C8903"
fee_staked_glp = w3.eth.contract(address=address_fee_staked_glp, abi=abi_usdc)
glp = w3.eth.contract(address=address_glp, abi=abi_glp)

# Read balances
balance_fee_staked_glp = fee_staked_glp.functions.balanceOf(address).call()
supply_glp = glp.functions.totalSupply().call()
my_percentage = balance_fee_staked_glp / supply_glp

print("My balance in the GMX Vault:")
for token in gmx_vault_address_list:
    gmx_vault_address_list[token]["my_balance"] = (
        my_percentage * gmx_vault_address_list[token]["gmx_vault_supply"]
    )
    print(f"{gmx_vault_address_list[token]['my_balance']} {token}")

print(supply_glp / 10**18)
print(balance_fee_staked_glp / 10**18)
