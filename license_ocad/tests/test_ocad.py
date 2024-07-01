import hashlib


# Get hash string
def hash_of_string(s):
    return hashlib.sha1(s.encode("utf-16-le")).hexdigest().upper()


# Convert hex to integer
def hex_to_int(s):
    hx = 0
    s = s.upper()
    slist = list(s)
    for c in slist:
        hx = hx * 16
        if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            hx = hx + ord(c) - ord("0")
        else:
            hx = hx + ord(c) - ord("A") + 10
        # print(c+" .. "+ str(hx)  +"--- "+ str(ord(c)) )
    return hx


def uppercase(oldStr: str):
    newStr = ""
    for c in oldStr:
        if "a" <= c <= "z":
            newStr += chr(ord(c) - 32)
        else:
            newStr += c
    return newStr


# Get key byte
def pkv_get_key_byte(seed, a, b, c):
    a = a % 25
    b = b % 3
    if a % 2 == 0:
        return (((seed >> a) & 0x000000FF) ^ ((seed >> b) | c)) & 0x000000FF
    else:
        return (((seed >> a) & 0x000000FF) ^ ((seed >> b) & c)) & 0x000000FF


# Get OCAD2018 checksum
def get_ocad2018_checksum(v, lnum, e, lname):

    slist = list(e)
    checksum = list("____-____-____")

    for i in [5, 6, 7, 8, 10, 11]:
        slist = list(
            hash_of_string(
                "".join(slist).upper() + uppercase(lname) + str(lnum) + uppercase(lname)
            )
        )
        # print(''.join(slist))
        idx = (v * (i + 1) + lnum) % 40
        # print(idx)
        checksum[i] = slist[idx]

    # print(checksum)

    s = (
        checksum[5]
        + checksum[6]
        + checksum[7]
        + checksum[8]
        + checksum[10]
        + checksum[11]
    )
    # print(s)
    a = pkv_get_key_byte(hex_to_int(s), lnum % 256, v % 2000, 13)
    # a = pkv_get_key_byte(8406981, ln % 256, v % 2000, 13)
    sl = list("{0:02X}".format(a))
    checksum[12] = sl[0]
    checksum[13] = sl[1]
    # print(checksum)

    s = "".join(checksum).replace("_", "")
    s = s.replace("-", "")

    slist = list(s)
    # print(s)

    slist = list(
        hash_of_string(e + "".join(slist).upper() + str(lnum) + uppercase(lname))
    )
    checksum[0] = slist[8]
    checksum[1] = slist[23]
    checksum[2] = slist[12]
    checksum[3] = slist[16]
    # print(checksum)
    return checksum


# Version = OCAD 2018 Orienteering
# Name = OL Ishikawa
# Number = 19277
# Checksum = BB83-215D-EE94
# Download link = https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e=ORI&l=19277&v=2018&d=un8ifnoj

checksum = "".join(
    get_ocad2018_checksum(
        2018,
        int("19277"),
        "Orienteering",
        "OL Ishikawa",
    )
)
print(checksum)
print("BB83-215D-EE94" == checksum)

# Version = OCAD 2018 Orienteering
# Name = OL Ishikawa
# Number = 19278
# Checksum = C130-69AF-D0FA
# Download link = https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e=ORI&l=19278&v=2018&d=v78pM3ZH

checksum = "".join(
    get_ocad2018_checksum(
        2018,
        int("19278"),
        "Orienteering",
        "OL Ishikawa",
    )
)
print(checksum)
print("C130-69AF-D0FA" == checksum)

# Version = OCAD 2018 Orienteering
# Name = Tsukuba44comp
# Number = 25664
# Checksum = 6E9D-030B-ADA1
# Download link = https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e=ORI&l=25664&v=2018&d=hhXX9wux

checksum = "".join(
    get_ocad2018_checksum(
        2018,
        int("25664"),
        "Orienteering",
        "Tsukuba44comp",
    )
)
print(checksum)
print("6E9D-030B-ADA1" == checksum)

# Version = OCAD 2018 Orienteering
# Name = Tsukuba44comp
# Number = 25665
# Checksum = 743D-1013-5624
# Download link = https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e=ORI&l=25665&v=2018&d=LYZ39ruh

checksum = "".join(
    get_ocad2018_checksum(
        2018,
        int("25665"),
        "Orienteering",
        "Tsukuba44comp",
    )
)
print(checksum)
print("743D-1013-5624" == checksum)

# Name = Långhundra IF
# Number = 5323
# Checksum Admin = 8EF8-7CFA-3E4B

checksum = "".join(
    get_ocad2018_checksum(
        2018,
        int("5323"),
        "Orienteering",
        "Långhundra IF",
    )
)
print(checksum)
print("8EF8-7CFA-3E4B" == checksum)
