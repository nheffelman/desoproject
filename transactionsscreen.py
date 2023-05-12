from kivymd.uix.screen import MDScreen
import pickle
import os
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivy.properties import BooleanProperty

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
    transaction_dialog = BooleanProperty()

    
    def transaction_dialog_switch(self, checkbox, value):
              
        if value:
            self.transaction_dialog = True            
            print('The checkbox', checkbox, 'is active')
        else:
            self.transaction_dialog = False
            print('The checkbox', checkbox, 'is inactive')
        settings = unpickle_settings()
        settings['transaction_dialog'] = self.transaction_dialog
        pickle_settings(settings)

    def on_enter(self):
        transactions = unpickle_transactions()
        
        settings = unpickle_settings()
        #toggle the transaction dialog switch
        if 'transaction_dialog' in settings:
            self.transaction_dialog = settings['transaction_dialog']
            if self.transaction_dialog:
                self.ids.transaction_dialog_switch.active = True
        
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
                    


        
    