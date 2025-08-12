#include "celdas.h"
#include "menu.h"
#include "estadisticas.h"

int main(int argc, char* argv[])
{
    char nombre_usuario[MAX_NOMBRE];
    int continuar;

    while (1)
    {
        continuar = mostrarMenuInicio(nombre_usuario, MAX_NOMBRE);

        if (continuar == -1)
        {
            // El usuario cerró la ventana del menú
            break;
        }

        jugarPartida(nombre_usuario, continuar);
    }

    printf("\nSaliendo del juego. \nHasta luego\n");
    return 0;
}
