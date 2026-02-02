import base64
import struct

# First ~1KB of body provided by user
# Removed headers, just body start
blob = """0000000950<H~3E88JNLNn7Na7n^2<z)v1nDL0rX&VT8Y&e6wHcxeCt000dDb8~4rVQz13d2MfXa{vGU
1JDNn02u%TM^8ai5l3%iWMy-6AV*I@R3IZbF*pDK(FXwl6aWzbM{i_gWpi^NM^8aiAR{<2H~=;X0RUNv
0RR910R%@+K~w<|M{i_gWpi^NM^8aiAR{<2H~;|!X>DO=WdQ_gaAjuz&4~Zl|JwjV01XKW3knDg3knMk
4h;_zAQcl55)&sJ9v2`kDKRiEDJ?8BI!Zn>HbyrrEkIX6ModmpQ&KWMT47pHU`kO^PygEhLjevB4iga*
CKVMXPc<zyPft%zPft%zPft%zPft%zPft%zPft%zPft%zPft%zPft%zPft%zPft%zPft%zPf!2A01*fQ
kO7bb0U`hb5di}c0sq7R8vp<T0|5a60000000000000C90s{sC00;lX08bDA0s#X71q25L1_22M1_J>B
0s{a95d{(<F+ouV6Jc=_A~J!Ip|K-EQo+#`Gh%Y#@FX-tQ)7aXqO$P^79~V;bS5=6le5B9WYXgQ!~hxr
00IL60RR9100000000000|WsA1po&B!~il800II51OWpB0|EvE0RR910RjL65d;z;F+md|Q3Wz#agnhj
ffO^L!Qt=~LecU6+5ij#0RRFK0}%i}09jqDCxM}C9qM=*tX9A|j1?+yW$?a6$>J(bx!yR?*}=%G(olCc
<5eRZ!y|$)X9n&yHK|}8H8qc+uFSFG69esxA8YGUc~K{h7WU)>uezy4BA4nH4w}8Zgk>NLw11fXlqML0
eMZqV5M0Ry;p->iHDuG;-7ng0M&pBHG%Grt!0)Qas_YreVMsHqyDxys!>FmKs>d3dnzXT(#>GxS!RjbW
SsA;3r<P(*qqyF4$*MQkt!N@x?c|<Gn`IF=lS095+Gf_E)h+Zwj|vr4nBWj|$0Qzf8wkcCI+t8+^E6tb
m%F+_#j*#yQVTTJZ7iX;TL>IPfkE$pCXJHAwii=0(x#nmT;%0}$JV9$C$u1X`o@^2rp|vVkmC_H3f;;y
t82*audZ()SWM*zRei1l6=!R=_H#}D0N#(zy4rVW)OwnRmoJ**@}V_LPSf7l!D%g}jHwKwRWM36i5$0|
8s=<_PRQys&hzI&YC42g7RFgUW;>Aw7C)r}HnjF`(dt@##jM!KQa3k|qO?siYm1fDwN?95z6eO&801Ln
)8kex#}UW8ZT22vIu4U8a-COH8&|TAQ3%}%o>=5@@c7dX&Wv`yTgMHEew0L$!vZwd5~@cS+Gb<Im-agG
H4f2g_fa8KbdO{=91Yw46er+BOJ%V&XVz@;2NjOe6rCp64s9?00F|p*B%f*#cn05DeIyg4!H>l+{{WS$"""

# Join into single line
cleaned = blob.replace("\n", "")

print(f"Cleaned len: {len(cleaned)}")

def try_decode(name, data, adobe):
    try:
        decoded = base64.a85decode(data, adobe=adobe)
        print(f"--- {name} ---")
        hex_dump = decoded[:100].hex()
        print(f"Hex: {hex_dump}")
        
        # Look for headers
        if b'\xff\xd8\xff' in decoded:
            print("FOUND JPEG MAGIC BYTES (FFD8FF)!")
            idx = decoded.find(b'\xff\xd8\xff')
            print(f"Offset: {idx}")
        elif b'\x89PNG' in decoded:
            print("FOUND PNG MAGIC BYTES!")
            idx = decoded.find(b'\x89PNG')
            print(f"Offset: {idx}")
        else:
            print("No simple Magic Bytes found in first chunk.")
            
    except Exception as e:
        print(f"--- {name} FAILED ---")
        print(e)

# 1. Try standard base64.a85decode (Ascii85)
try_decode("Standard Ascii85 (adobe=False)", cleaned, False)

# 2. Try Adobe style (wrap with <~ ~>)
wrapped = "<~" + cleaned + "~>"
try_decode("Adobe Ascii85 (adobe=True)", wrapped, True)

# 3. Try Base85 (RFC 1924) - separate function
print("--- Base85 (RFC1924) ---")
try:
    decoded_b85 = base64.b85decode(cleaned)
    print(f"Decoded {len(decoded_b85)} bytes total")
    print(f"First 100 bytes: {decoded_b85[:100].hex()}")
    
    # SCAN ENTIRE BINARY FOR IMAGES
    print("\n🔍 Scanning for image magic bytes...")
    
    # Search for JPEG (FF D8 FF)
    jpeg_offsets = []
    for i in range(len(decoded_b85) - 3):
        if (decoded_b85[i] == 0xFF and decoded_b85[i+1] == 0xD8 and 
            decoded_b85[i+2] == 0xFF):
            jpeg_offsets.append(i)
    
    if jpeg_offsets:
        print(f"\n✅ JPEG FOUND at offsets: {jpeg_offsets}")
        for offset in jpeg_offsets:
            # Save the image
            img_path = f'/tmp/extracted_{offset}.jpg'
            with open(img_path, 'wb') as f:
                f.write(decoded_b85[offset:])
            print(f"   Saved {len(decoded_b85[offset:])} bytes to {img_path}")
            print(f"   Header: {decoded_b85[offset:offset+20].hex()}")
    else:
        print("❌ No JPEG headers found")
    
    # Search for PNG (89 50 4E 47)
    png_offsets = []
    for i in range(len(decoded_b85) - 4):
        if (decoded_b85[i] == 0x89 and decoded_b85[i+1] == 0x50 and 
            decoded_b85[i+2] == 0x4E and decoded_b85[i+3] == 0x47):
            png_offsets.append(i)
    
    if png_offsets:
        print(f"\n✅ PNG FOUND at offsets: {png_offsets}")
        for offset in png_offsets:
            img_path = f'/tmp/extracted_{offset}.png'
            with open(img_path, 'wb') as f:
                f.write(decoded_b85[offset:])
            print(f"   Saved {len(decoded_b85[offset:])} bytes to {img_path}")
            print(f"   Header: {decoded_b85[offset:offset+20].hex()}")
    else:
        print("❌ No PNG headers found")
        
except Exception as e:
    print(f"--- Base85 FAILED ---: {e}")
