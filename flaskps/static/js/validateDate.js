function validate(){
    alert("Usando validate ")
    fechas = document.querySelectorAll('input[type="date"]')    
    fecha_ven = new Date(fechas[0].value)
    fecha_hoy = new Date()    
    if (fecha_ven < fecha_hoy){
        alert("La tarjeta ingresada está vencida. No puede utilizarse")
        return false
    }    
    return true

}
function validateDate(){
    
    fechas = document.querySelectorAll('input[type="date"]')    
    fecha_ven = new Date(fechas[0].value)
    fecha_hoy = new Date()    
    if (fecha_ven < fecha_hoy){
        alert("La tarjeta ingresada está vencida. No puede utilizarse")
        return false
    }    
    return true

}