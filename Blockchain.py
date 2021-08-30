#Prototyp einer simplen Blockchain in Python
#MSD 19- Seminar/ Ulrike Ozim

#notwendige imports
#hashlib: encryption
#JSON für die Formatierung
#time: für den timestamp

import hashlib
import json
from time import time

# Blockchain-Klasse erstellen:
# chain: in die Chain (leere Liste) werden die einzelnen Blocks hinzugefügt
# pending_ransactions: == eine noch nicht bestätigte Transaktion in einem Array gespeichert, sie ist noch nicht Teil eines
#   Blocks.
# new_block: damit werden die Blöcke der Blockchain hinzugefügt.

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.",
                       proof=100)

    # die Funktion für die Erstellung eines neuen Blocks
    # Ein neuer Blockeintrag wird als JSON Objekt erstellt.
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,  # die Länge der Blockchain wird um 1 verlängert, jeder Block erhält einen Index
            'timestamp': time(),    # jeder Block hat einen timestamp, der Zeitpunkt der confirmation ist sichtbar
            'transactions': self.pending_transactions,  # die pending_transactions werden einem Block hizugefügt.
            'proof': proof, # der PoW ist bestätigt
            'previous_hash': previous_hash or self.hash(self.chain[-1]), #der vorherige, bestätigte Hash.
        }
        # die Liste der pending_transactions zurücksetzen, der neueste Block wird hinzugefügt.
        self.pending_transactions = []
        self.chain.append(block)

        return block

    # Methode mit der der letzte/aktuellste Block ausgegeben wird:
    @property
    def last_block(self):
        return self.chain[-1]

    # die Transaktion im Pool 'anmelden', sie wird zunächst eine 'pending_transaction'.
    # die 3 Variablen für die Transaktion sind sender, recipient und amount
    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        #die pending_transaction als JSON-Objekt; sie 'wartet' bis ein neuer Block geschürft wird.
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1     #der Index des Blocks zu dem die neue transaction hinzugefügt wird.

    # receive one block. Turn it into a string,
    # turn that into Unicode (for hashing).

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)   #key-value Paare werden in Strings umgewandelt
        block_string = string_object.encode()   #in Unicode umgewandelt

        raw_hash = hashlib.sha256(block_string) #gehasht mit SHA256 encryption (siehe import)
        hex_hash = raw_hash.hexdigest() #in hexadeciaml String umgewandelt

        return hex_hash #neuer Hash

#eine neue Instanz wird initialisiert
blockchain = Blockchain()

#ein paar Transaktionen werden hinzugefügt
t1 = blockchain.new_transaction("Satoshi", "Jack", '1 BTC')
t2 = blockchain.new_transaction("Jack", "Satoshi", '2 BTC')
t3 = blockchain.new_transaction("Satoshi", "Alan", '3 BTC')
blockchain.new_block(12345)

t4 = blockchain.new_transaction("Jack", "Alice", '4 BTC')
t5 = blockchain.new_transaction("Alice", "Bob", '5 BTC')
t6 = blockchain.new_transaction("Bob", "Jack", '6 BTC')
blockchain.new_block(6789)

print("Genesis block: ", blockchain.chain)