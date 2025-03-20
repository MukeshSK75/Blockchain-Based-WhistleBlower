from bitcoinlib.keys import Key

def bitcoin_random_key_with_address():
    # Generate a random Bitcoin key
    key = Key()
    private_key_hex = key.private_hex
    bitcoin_address = key.address
    return private_key_hex, bitcoin_address

# Generate a random Bitcoin private key and address
random_private_key, bitcoin_address = bitcoin_random_key_with_address()
print("Random Bitcoin Private Key:", random_private_key)
print("Bitcoin Address:", bitcoin_address)