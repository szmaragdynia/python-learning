print("---->\n\n")

def powiedz_hej(powitanie = "siema", imie = "eniu"):
    print(powitanie +" " + imie)
    return True
    print("tego nei napisze")

cos_narobil = powiedz_hej()
print(cos_narobil)
powiedz_hej("elo","ziomie")

print("\n-------------\n")

is_happy = False
if is_happy and cos_narobil: 
    print("ify działajo")
elif not is_happy and not cos_narobil:
    print ("ify dalej działajo")
else: 
    print("cos sie skwisiło")




print("\n-------------\n")


pozwolenia_na = {
    "bron": True,
    "zycie": 75,
    "trzypsy": [True, True, False],
    69: "mama zabrania"
}

print(pozwolenia_na)
print(pozwolenia_na["bron"])
print(pozwolenia_na.get("bron"))

print(pozwolenia_na.get("adsad"))
    #print(pozwolenia_na["asdassad"]) to juz sypie errorem
print(pozwolenia_na.get("adsad", "costy panie wpisal"))
print(pozwolenia_na[69])

print("\n\n<-----")