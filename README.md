# Narwhallet - alpha
## **UN-Official** Kevacoin ElectrumX Wallet

### Please Note
This project currently in **alpha**.

Project was originally built for fun from manually deconstructing, *made* to work with localized cases...

That means this is a **work-in-progress**. While in alpha project will be undergoing large amounts of cleanup and refactors.

Please proceed with caution because things probably will be a bit unstable. If a crash or other unintended result does occur, please report it so it can be addressed!

Until initial beta release recommended to use a read-only or watch wallet.


## Setup
*recommended to use a virtual environment for separation and to ensure no dependency conflicts*

### venv example
mkdir K1<br/>
cd K1<br/>
python3 -m venv ./venv<br/>
source ./venv/bin/activate<br/>

### Download repo & Install requirements
git clone https://github.com/kevaone/narwhallet.git<br/>
cd narwhallet<br/>
pip install -r ./requirements.txt<br/>

### Launch
python3 ./narwhallet_gui.py

**Upon launch Narwhallet will create the directory .narwhalllet within you're home directory. You're wallets, address book, settings and cache are saved here.**

After initial launch of narwhallet.py, Narwhallet Web may be launched.

python3 ./narwhallet_web.py

Once web launched can navigate to http://localhost:8099/

It is also highly recommended you run your own instance of ElectrumX. If you have large wallets or large number of wallets you will probably be throttled updating against public peers; Running your own ElectrumX you can adjust for your needs.

Can download ElectrumX here: https://github.com/kevacoin-project/electrumx


## Wallets Supported

### Normal Wallets
Create or restore mnemonic phrase for bip49 based wallet

### Read Only Wallet
Restore an ypub or track wallet addresses

### Watch Wallet
Track individual addresses

**Important Notes**
The default ElectrumX peer, kex.keva.one, currently *does not support IPFS uploads*.

While experimenting with alpha perform initial sych with the default peer unless running your own. Initial tx/ns cache building will be getting refined further to reduce calls and load to allow faster synch.

While Narhwallet Web looks like https://keva.one it is different. Narhwallet Web is being rewritten to be more of an local ad-hoc experience.
