import webbrowser



#open a browser to deso.identtity.com and open the login page which returns a token
response = webbrowser.open('https://identity.deso.org/derive?javascript=True')
print(response)

