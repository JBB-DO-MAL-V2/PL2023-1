import re

def print_res(line: str):
  print("maq: " + line)

def valid_coin(coin: str):
  # only accepts 5c or above
  return (re.match(r"(5|10|20|50)c", coin) != None) or (re.match(r"(1|2)e", coin) != None)

def coin_balance(coin: str):
  if coin == "5c":
    return 0.05
  elif coin == "10c":
    return 0.10
  elif coin == "20c":
    return 0.20
  elif coin == "50c":
    return 0.50
  elif coin == "1e":
    return 1.00
  elif coin == "2e":
    return 2.00
  return 0.00

def add_balance(coins: str):
  balance = 0.0
  all_coins = coins[6:].split(',')
  for c in all_coins:
    c = c.strip()
    if valid_coin(c):
      balance += coin_balance(c)
    else:
      print_res(c + " - moeda inválida")
  return balance

def make_call(number: str, balance: float):
  out = 0
  number = number[2:]
  print(number)
  if re.match(r"(601|641)\d+",number) != None: # blocked numbers
    print_res("Esse número não é permitido neste telefone. Queira discar novo número!")
  elif re.match(r"(00)\d+",number) != None: # international line
    if balance >= 1.50:
      balance -= 1.50
    else:
      print_res("Não possui saldo suficiente. Queira inserir mais moedas e discar novamente!")
  elif re.match(r"(2)\d+",number) != None and len(number) == 9: # national line
    if balance >= 0.25:
      balance -= 0.25
    else:
      print_res("Não possui saldo suficiente. Queira inserir mais moedas e discar novamente!")
  elif re.match(r"(800)\d+",number) != None and len(number) == 9: # green line
    balance -= 0.00
  elif re.match(r"(808)\d+",number) != None and len(number) == 9: # blue line
    if balance >= 0.10:  
      balance -= 0.10
    else:
      print_res("Não possui saldo suficiente. Queira inserir mais moedas e discar novamente!")
  else: # invalid numbers
    print_res("Esse número é inválido ou não existe. Queira discar novo número!")
  return balance

def balance_splitter(balance: float):
  balance_str = str(balance)
  balance_splited = balance_str.split(".")
  return balance_splited[0]+"e"+balance_splited[1]+"c"

def print_balance(balance: float):
  print_res("saldo = " + balance_splitter(balance))

def change(balance: float, out: bool):
  map_coins = {"5c": 0, "10c": 0, "20c": 0, "50c": 0,"1e": 0, "2e": 0}
  print(balance)
  while balance != 0.00:
    if balance >= 2.00:
      map_coins["2e"] += 1
      balance -= 2

    elif balance >= 1.00:
      map_coins["1e"] += 1
      balance -= 1

    elif balance >= 0.50:
      map_coins["50c"] += 1
      balance -= 0.5

    elif balance >= 0.20:
      map_coins["20c"] += 1
      balance -= 0.2

    elif balance >= 0.10:
      map_coins["10c"] += 1
      balance -= 0.1

    elif balance >= 0.05:
      map_coins["5c"] += 1
      balance -= 0.05

    # print(balance)

  coins_change = ""
  for k,v in map_coins.items():
    if v != 0:
      coins_change = coins_change + ", " + str(v) + "x" + k
  
  coins_change = coins_change[1:]

  if out:
    print_res("troco =" + coins_change)
    print_res("Volte sempre!") 
  else:
    print_res("Tome os seus " + balance_splitter(balance) + " de volta!")
    print_res("Volte sempre!")

def main():
  ins = str(input())
  balance = 0.00
  out = True
  if re.fullmatch(r"(?i:LEVANTAR)", ins):
    print_res("Introduza moedas!")
    ins = str(input())

    if re.match(r"(?i:MOEDA)", ins):
      balance += add_balance(ins)
      print_balance(balance)

      ins = str(input())

      while re.fullmatch(r"(?i:POUSAR)", ins) == None:
        # using if statements because match is for 3.10+ python version
        if re.match(r"(?i:MOEDA)", ins):
          balance += add_balance(ins)
          print_balance(balance)

        elif re.match(r"(?i:T=)", ins):
          balance = make_call(ins, balance)
          print_balance(balance)
            
        elif re.match(r"(?i:ABORTAR)", ins):
          out = False
          break

        else:
          print_res("Ação inválida ou inexistente!")

        ins = str(input())

    else:
      print("Precisa de inserir moedas primeiramente!")

    change(balance, out)

  else:
    print("Ação inválida ou inexistente!")
    
if __name__ == "__main__":
  main()