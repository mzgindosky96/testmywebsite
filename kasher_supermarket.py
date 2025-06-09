# سیستمێ کاسێر بە کوردی-سۆرانی
# نووسراو لەلایەن: سوپەرمارکێتێ [ناوی سوپەرمارکێتێ خۆت] - هەولێر

kallakan = []  # لیستێ کاڵاکان
gshty_nrx = 0  # نرخی گشتی

print("بەخێربێن بۆ سیستمێ کاسێری سوپەرمارکێتێ [ناوی سوپەرمارکێت]!")
print("-----------------------------------------------")

while True:
    nav = input("ناوی کاڵا (بە کوردی): ")
    nrx_yek = float(input("نرخی تاک (دینار): "))
    jmare = int(input("ژمارە: "))
    
    koste = nrx_yek * jmare
    kallakan.append((nav, nrx_yek, jmare, koste))
    gshty_nrx += koste
    
    dewam = input("کاڵای تر هەیە؟ (بەڵێ/نەخێر): ")
    if dewam.lower() == "نەخێر" or dewam.lower() == "n":
        break

# پوختەی پسوڵە
print("\nپسوڵە:")
print("-----------------------------------------------")
print("کاڵا | نرخی تاک | ژمارە | کۆست")
print("-----------------------------------------------")
for kallak in kallakan:
    print(f"{kallak[0]} | {kallak[1]:,} د.ع | {kallak[2]} | {kallak[3]:,} د.ع")

print("-----------------------------------------------")
print(f"نرخی گشتی: {gshty_nrx:,} دیناری عێراقی")

# پارەدان
while True:
    pare_da = float(input("\nبڕی پارە دەدەیت (دینار): "))
    if pare_da >= gshty_nrx:
        mayw = pare_da - gshty_nrx
        print(f"\nپارە ماوە: {mayw:,} دیناری عێراقی")
        print("سوپاس بۆ کڕین! بەزەیی بکەرەوە :)")
        break
    else:
        print(f"پارە کەمە! زیاتر بکەوە {gshty_nrx - pare_da:,} دینار")