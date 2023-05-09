from kivymd.uix.screen import MDScreen
import pickle
import os
from kivymd.toast import toast
from kivymd.uix.label import MDLabel

#pickles the current settings
def pickle_settings(settings):
    with open('temp/settings.pickle', 'wb') as handle:
        pickle.dump(settings, handle, protocol=pickle.HIGHEST_PROTOCOL)

#unpickles the current settings
def unpickle_settings():
    if os.path.exists('temp/settings.pickle'):
        with open('temp/settings.pickle', 'rb') as handle:
            settings = pickle.load(handle)
    else:
        settings = {}  
    return settings

#pickles transactions
def pickle_transactions(transactions):
    with open('temp/transactions.pickle', 'wb') as handle:
        pickle.dump(transactions, handle, protocol=pickle.HIGHEST_PROTOCOL)

#unpickles transactions
def unpickle_transactions():
    if os.path.exists('temp/transactions.pickle'):
        with open('temp/transactions.pickle', 'rb') as handle:
            transactions = pickle.load(handle)
    else:
        transactions = {}  
    return transactions

class TransactionsScreen(MDScreen):

    
    
    def on_enter(self):
        transactions = unpickle_transactions()
        
        settings = unpickle_settings()
        if 'publicKey' not in settings:
            toast('Please login to view transactions')
            
        else: 
            publicKey = settings['publicKey']
            print('publicKey', publicKey)

            if publicKey not in transactions:
                toast('No transactions found')
                print('no transactions found')
            else:
                publicKeyTransactions = transactions[publicKey]
                self.ids.mainLayout.clear_widgets()
                publicKeyTransactions.reverse()
                for transaction in publicKeyTransactions:
                    
                    label = MDLabel(text=str(transaction), halign='center', adaptive_height=True)
                    self.ids.mainLayout.add_widget(label)
                    


        
    