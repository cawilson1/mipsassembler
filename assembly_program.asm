Label1:




asdf
j Label2:
jal 80000
j Label1:
j Label1:
sll $t5, $s5, 3
srl $t5, $s5, 31
srl $t5, $s5, 32
bne $t7, $t7, 9876543
bne $t7, $t7, -345678
add $s0, $s0, $s0
sub $t4, $s6, $s6
addi $s2, $s0, 256
and $t4, $s2, $t3
or $t5, $zero, $s7
xor $t8, $zero, $v1
nor $s6, $s6, $s6
bne $t7, $t7, 255
add $s0, $s0, $s0
beq $s0, $t0, 511
add $s0, $s0, $s0
bne $s1, $t0, -5
j Label2:
jal 7
lw $s0, 8($s3)
lb $s1, 8($s4)
lh $s1, 8($s4)
POOP:
sw $t7, 12($t5)
sb $t7, 12($t5)
sh $t7, 12($t5)
bne $15, $15, 255
bne $t7, $t7, 255
add $0, $zero, $0
slti $t5, $s7, 9
Label2:
Label3
andi $a0, $a0, 15
ori $s0, $a0, 255
xori $s0, $a0, 255
lui $s7 7
jr $s7
mult $s7, $s6
div $s7, $s6
syscall
