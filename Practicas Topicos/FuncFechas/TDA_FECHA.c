#include "Primitivas.h"

const int diasMes[12] = {31,28,31,30,31,30,31,31,30,31,30,31};

int esBisiesto(int anio) {
    int result;
    if((anio % 4 == 0 && anio % 100 != 0) || (anio % 100 == 0 && anio % 400 == 0)) {
        result = 1;
    }
    else {
        result = 0;
    }
    return result;
}

int diasHastaFin(tFecha f) {
    int cantDiasMes = diasMes[f.mes - 1];
    cantDiasMes -= f.dia;
    return cantDiasMes;
}

char cantidadDias(tFecha fecha)
{
    char r;
    if(fecha.mes == 1 || fecha.mes == 3 || fecha.mes == 5 || fecha.mes == 7 || fecha.mes == 8 || fecha.mes == 10 || fecha.mes == 12)
        r=31;
    else if(fecha.mes == 4 || fecha.mes == 6 || fecha.mes == 9 || fecha.mes == 11)
        r=30;
    else
        r=28;

    return r;
}

int esFechaValida(tFecha f) {
    char result = 0;
    int temp;
    if((f.anio > 1600) && (f.mes > 0 && f.mes < 13)) {
        temp = cantidadDias(f);
        if(esBisiesto(f.anio) && f.mes == 2)
            temp++;
        if(f.dia > 0 && f.dia <= temp)
            result = 1;
    }
    return result;
}

tFecha IngresarFecha() {
    tFecha fecha;
    printf("Ingrese fecha en formato dd/mm/aaaa \n");
    char num = scanf("%d/%d/%d", &fecha.dia, &fecha.mes, &fecha.anio);
    while (!(esFechaValida(fecha)) || num < 3) {
        printf("Fecha Incorrecta. Ingrese fecha en formato dd/mm/aaaa \n");
        scanf("%d/%d/%d", &fecha.dia, &fecha.mes, &fecha.anio);
    }
    return fecha;
}

int diaDelAnio(tFecha fecha) {
    int suma = 0;
    int cont = 0;
    while(cont < fecha.mes - 1) {
        suma += diasMes[cont];
        cont += 1;
    }
    if(esBisiesto(fecha.anio) && fecha.mes > 2) {
        suma += 1;

    }
    suma += fecha.dia;
    printf("el dia del anio es %d", suma);
    return suma;
}

void sumarDias(tFecha fecha, int dias) {
    int temp;
    while (dias > 0) {
        temp = diasHastaFin(fecha);
        if(dias > temp) {
            fecha.dia = 1;
            fecha.mes += 1;
            if(fecha.mes > 12) {
                fecha.anio += 1;
                fecha.mes = 1;
            }
            temp++;
            dias -= temp;
        }
        else {
            fecha.dia += dias;
            dias = 0;
        }
    }
    printf("Nueva fecha %d/%d/%d", fecha.dia, fecha.mes, fecha.anio);

}

int contarDias(tFecha f) {
    int total = f.dia;

    // Sumar días de los meses anteriores en el mismo año
    for (int i = 0; i < f.mes - 1; i++) {
        total += diasMes[i];
    }

    // Agregar 1 día si el año es bisiesto y ya pasó febrero
    if (f.mes > 2 && esBisiesto(f.anio)) {
        total += 1;
    }

    // Sumar días de los años anteriores
    for (int i = 1600; i < f.anio; i++) {
        total += esBisiesto(i) ? 366 : 365;
    }
    return total;
}


int diferenciaFechas(tFecha fechaUno, tFecha fechaDos) {
    int dias1 = contarDias(fechaUno);
    int dias2 = contarDias(fechaDos);
    return abs(dias1 - dias2);
}
