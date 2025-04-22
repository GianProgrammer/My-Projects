// CLASE TDA
typedef struct {
    int dia;
    int mes;
    int anio;
} tFecha;


int esBisiesto(int a);
int diasHastaFin(tFecha f);
int esFechaValida(tFecha f);
tFecha IngresarFecha();
int diaDelAnio(tFecha f);
void sumarDias(tFecha f, int d);
int contarDias(tFecha f);
int diferenciaFechas(tFecha f, tFecha f2);
