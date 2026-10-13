	.syntax unified
	.section .text
	.align 2
	.arm
	.global AraunaOpening_DecodeTiles
	.global AraunaOpening_DecodeTilesEnd
	.type AraunaOpening_DecodeTiles, %function
AraunaOpening_DecodeTiles:
	stmdb sp!, {r4-r11, lr}
	mov r4, #600
	mov r5, #30
1:
	ldrb r2, [r0], #1
	mov r3, r0
	add r0, r0, r2
	mov r6, #3
	cmp r2, #4
	movle r6, #2
	cmp r2, #2
	movle r6, #1
	cmp r2, #1
	moveq r6, #0
	mov r7, #1
	mov r7, r7, lsl r6
	sub r7, r7, #1
	mov r11, r1
	mov r8, #8
	cmp r6, #0
	beq 4f
2:
	mov r9, #0
	cmp r6, #1
	ldrbge r9, [r0], #1
	cmp r6, #2
	ldrbge r2, [r0], #1
	orrge r9, r9, r2, lsl #8
	cmp r6, #3
	ldrbeq r2, [r0], #1
	orreq r9, r9, r2, lsl #16
3:
	and r2, r9, r7
	ldrb r2, [r3, r2]
	mov r9, r9, lsr r6
	and r12, r9, r7
	ldrb r12, [r3, r12]
	orr r2, r2, r12, lsl #8
	mov r9, r9, lsr r6
	strh r2, [r1], #2
	and r2, r9, r7
	ldrb r2, [r3, r2]
	mov r9, r9, lsr r6
	and r12, r9, r7
	ldrb r12, [r3, r12]
	orr r2, r2, r12, lsl #8
	mov r9, r9, lsr r6
	strh r2, [r1], #2
	and r2, r9, r7
	ldrb r2, [r3, r2]
	mov r9, r9, lsr r6
	and r12, r9, r7
	ldrb r12, [r3, r12]
	orr r2, r2, r12, lsl #8
	mov r9, r9, lsr r6
	strh r2, [r1], #2
	and r2, r9, r7
	ldrb r2, [r3, r2]
	mov r9, r9, lsr r6
	and r12, r9, r7
	ldrb r12, [r3, r12]
	orr r2, r2, r12, lsl #8
	mov r9, r9, lsr r6
	strh r2, [r1], #2
	add r1, r1, #232
	subs r8, r8, #1
	bne 2b
5:
	add r1, r11, #8
	subs r5, r5, #1
	addeq r1, r1, #1680
	moveq r5, #30
	subs r4, r4, #1
	bne 1b
	ldmia sp!, {r4-r11, lr}
	bx lr
4:
	ldrb r2, [r3]
	orr r2, r2, r2, lsl #8
	orr r2, r2, r2, lsl #16
6:
	str r2, [r1]
	str r2, [r1, #4]
	add r1, r1, #240
	subs r8, r8, #1
	bne 6b
	b 5b
AraunaOpening_DecodeTilesEnd:
	.size AraunaOpening_DecodeTiles, .-AraunaOpening_DecodeTiles
