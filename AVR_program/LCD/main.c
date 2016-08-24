/*
 * LCD.c
 *
 * Created: 8/6/2016 12:46:03 PM
 * Author : aayus
 */ 
#define F_CPU 16000000UL
#define Baud 9600
#define bauD ((((F_CPU)/16)/Baud)-1)

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "lcd.h"

//MOTOR DEFINATION
#define Motor_ddr DDRD
#define Motor_port PORTD
#define Motor1_Dir1 PD2
#define Motor1_Dir2 PD3
#define Motor2_Dir1 PD6
#define Motor2_Dir2 PD7
#define Motor1_pwm PD4
#define Motor2_pwm PD5

//light defination
#define Light_ddr DDRA
#define light_port PORTA 
#define L_Car_On PINA0 
#define L_Start PINA1 
#define L_Back PINA2 
#define L_Right PINA3 
#define L_Left PINA4 
#define L_Stop PINA5 
#define L_TX PINA6 
#define L_RX PINA7 

void disp_lcd(char *);
void Init_Pwm();
void forward_func();
void backward_func();
void left_func();
void right_func();
void stop_func();

unsigned char data=0;
unsigned char BUFFER=0;
unsigned char Forward_Flag=0;
unsigned char Stop_Flag=0;

char start[16] = {"---->>START<<---"};
char stop[16] = {"---->>STOP<<----"};
char left[16] = {"---->>LEFT<<----"};
char right[16] = {"---->>RIGHT<<---"};
char bac[16] = {"--->>BACK<<---"};
	
	
void USART_Init()
{
	UBRRL = bauD;
	UBRRH = (bauD>>8);
	UCSRB = ((1<<RXEN)|(1<<TXEN)|(1<<RXCIE)|(1<<TXCIE));
	UCSRC = ((1<<URSEL)|(1<<UCSZ0)|(1<<UCSZ1));
}

unsigned char USART_Receive( void )
{
	return BUFFER;
}

void USART_Transmit( unsigned char data )
{
	light_port |= (1<<L_TX);
	while ( !( UCSRA & (1<<UDRE)) );
	UDR = data;
	light_port &=~ (1<<L_TX);
}

int main(void)
{	
	Light_ddr |= ((1<<L_Car_On)|(1<<L_Start)|(1<<L_Back)|(1<<L_Right)|(1<<L_Left)|(1<<L_Stop)|(1<<L_TX)|(1<<L_RX));
	USART_Init();
	lcd_init();
	Init_Pwm();
	sei();
	disp_lcd(stop);
	
	while(1)
	{
		light_port |=(1<<L_Car_On);
		if (BUFFER=='f')
		{
			Forward_Flag=1;
			forward_func();
		}
		else if ((BUFFER=='l')&&(Forward_Flag))
		{
			light_port &=~ (1<<L_Right);
			light_port |= (1<<L_Left);
			left_func();
			_delay_ms(4000);
			BUFFER= 'f' ;
			light_port &=~ (1<<L_Left);
		}
		else if ((BUFFER=='r')&&(Forward_Flag))
		{		
			light_port &=~ (1<<L_Left);
			light_port |= (1<<L_Right);
			right_func();
			_delay_ms(4000);
			BUFFER='f';
			light_port &=~ (1<<L_Right);
		}
		else if (BUFFER=='q')
		{
			Stop_Flag=1;
			stop_func();
			Forward_Flag=0;
		}
		else if ((BUFFER=='b')&&(Stop_Flag))
		{
			light_port &=~ (1<<L_Stop);
			light_port |= (1<<L_Back);
			backward_func();
			_delay_ms(4000);
			BUFFER='q';
			light_port &=~ (1<<L_Back);
			light_port |= (1<<L_Stop);
		}
	}
}

void Init_Pwm()
{
	Motor_ddr |= ( (1<<Motor1_pwm) | (1<<Motor2_pwm) ); //ocr1b,ocr1a
	Motor_ddr |= ( (1<<Motor1_Dir1) | (1<<Motor1_Dir2) | (1<<Motor2_Dir1) | (1<<Motor2_Dir2));  //direction
	Motor_port &=~ ( (1<<Motor1_Dir1)|(1<<Motor1_Dir2)|(1<<Motor1_pwm)|(1<<Motor2_pwm)|(1<<Motor2_Dir1)|(1<<Motor2_Dir2));
	TCCR1A |= ( (1<<COM1A1) | (1<<COM1B1) | (1<<WGM11));
	TCCR1B |= ( (1<<CS10) | (1<<WGM12) | (1<<WGM13) );
	ICR1 = 3200;
}

void disp_lcd(char *data)
{
	lcd_clear();
	lcd_gotoxy(0,0);
	Printf("Say Smth......");
	lcd_gotoxy(0,1);
	Printf(data);
	_delay_ms(50);
}

void forward_func()
{
	disp_lcd(start);
	Motor_port |= ((1<<Motor1_Dir1)| (1<<Motor2_Dir1));
	Motor_port &= ~ ((1<<Motor1_Dir2)| (1<<Motor2_Dir2));
	OCR1A=1600;
	OCR1B=3000;
	light_port |= (1<<L_Start);
	light_port &=~ (1<<L_Stop);
}

void backward_func()
{
	disp_lcd(bac);
	Motor_port |= ((1<<Motor1_Dir2)| (1<<Motor2_Dir2));
	Motor_port &= ~ ((1<<Motor1_Dir1)| (1<<Motor2_Dir1));
	OCR1A=1600;
	OCR1B=3000;
}

void left_func()
{
	disp_lcd(left);
	Motor_port |= (1<<Motor1_Dir1);
	Motor_port &=~ (1<<Motor1_Dir2);
	Motor_port &=~ ((1<<Motor2_Dir2)|(1<<Motor2_Dir1));
	OCR1B=3000;
	OCR1A=0;
}

void right_func()
{
	disp_lcd(right);
	Motor_port |= ((1<<Motor2_Dir1));
	Motor_port &=~ ((1<<Motor2_Dir2));
	Motor_port &=~((1<<Motor1_Dir1)|(1<<Motor1_Dir2));
	OCR1B=0;
	OCR1A=1600;
}

void stop_func()
{
	disp_lcd(stop);
	Motor_port &=~((1<<Motor2_Dir1)|(1<<Motor2_Dir2)|(1<<Motor1_Dir1)|(1<<Motor1_Dir2));
	OCR1A=0;
	OCR1B=0;
	light_port &=~ (1<<L_Start);
	light_port |= (1<<L_Stop);
}

ISR (USART_RXC_vect)
{
	light_port |= (1<<L_RX);
	BUFFER=UDR;
	light_port &= ~(1<<L_RX);
}
