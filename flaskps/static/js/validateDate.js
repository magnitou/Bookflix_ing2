function validate(){
    fechas = document.querySelectorAll('input[type="date"]')
    fecha_ini = fechas[0].value
    fecha_fin = fechas[1].value
    if (fecha_fin < fecha_ini){
        alert("error en fechas")
        return false
    }
    return true

}