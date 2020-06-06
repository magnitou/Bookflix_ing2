function validate(){
    fechas = document.querySelectorAll('input[type="date"]')
    fecha_ini = fechas[0].value
    fecha_fin = fechas[1].value
    console.log(fecha_fin=='')
    if (fecha_fin!='' && fecha_fin < fecha_ini){
        alert("error en fechas")
        return false
    }
    return true

}
function validateDate(){
    
    fechas = document.querySelectorAll('input[type="month"]')  
    console.log(fechas[0].value)  
    fecha_ven = new Date(fechas[0].value)
    console.log(fecha_ven)
    fecha_hoy = new Date()    
    console.log(fecha_hoy)
    console.log(fecha_ven < fecha_hoy)
    if (fecha_ven < fecha_hoy){
        alert("La tarjeta ingresada está vencida. No puede utilizarse")
        return false
    }    
    return true

}