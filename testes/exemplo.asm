address 0

lcl_low r1, 5       # R1 = 5
lcl_low r2, 10      # R2 = 10

add r3, r1, r2      # R3 = R1 + R2 = 15

mult r4, r1, r2     # R4 = 5 * 10 = 50

loop:
    add r5, r5, r1  # R5 += 5
    beq r5, r2, fim # Se R5 == 10, vai para fim
    j loop

fim:
    halt