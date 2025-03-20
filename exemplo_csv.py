import csv


with open("exemplo_2.csv","w", newline="") as file:
     writer = csv.writer(file)
     writer.writerow(["nome","email","telefone"])
     writer.writerow(["Joao","joao@msn.com","(11) 9999-9999"])
     writer.writerow(["Maria","maria@msn.com","(13) 9999-9999"])
     writer.writerow(["Joao","joao@msn.com","(11) 9999-9999"])
     writer.writerow(["Maria","maria@msn.com","(13) 9999-9999"])