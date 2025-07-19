from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils import timezone
from .queryset import UsuarioQuerySet

def procesar_envio_recordatorios():
    usuarios = UsuarioQuerySet.usuarios_retiro_24_horas()
    ahora = timezone.now()

    for usuario in usuarios:
        fecha_registro = usuario['fecha_registro']
        if fecha_registro.tzinfo is None:
            fecha_registro = make_aware(fecha_registro)

        intervalo_dias = usuario.get('retiro_en_dias')
        if intervalo_dias is None or not isinstance(intervalo_dias, int) or intervalo_dias <= 0:
            print(f"❌ Usuario con datos inválidos: {usuario['correo']} | retiro_en_dias={intervalo_dias}")
            continue

        intervalo_dias = usuario['retiro_en_dias']
        tiempo_transcurrido = ahora - fecha_registro
        ciclos = tiempo_transcurrido.days // intervalo_dias
        proximo_retiro = fecha_registro + timedelta(days=(ciclos + 1) * intervalo_dias)
        tiempo_restante = proximo_retiro - ahora

        print(f"Correo: {usuario['correo']} | Próximo retiro: {proximo_retiro}")

        medicamentos_str = usuario.get('medicamentos', '')
        medicamentos = [
            m.strip() 
            for m in medicamentos_str.split(';') 
            if m.strip()
        ]

        lista_numerada = '\n'.join(
            f"{idx + 1}. {med}" 
            for idx, med in enumerate(medicamentos)
        )

        mensaje = (
            f"Hola {usuario['nombre']} {usuario['apellido']},\n\n"
            f"Recuerda que debes retirar tu medicamento antes del "
            f"{proximo_retiro.strftime('%d/%m/%Y %H:%M')}.\n\n"
            f"---\n"
            f"Medicamentos a retirar:\n"
            f"{lista_numerada}\n\n"
            f"Este mensaje es un recordatorio automático del sistema.\n\n"
            f"Saludos,\n"
            f"Equipo de Salud"
        )

        if timedelta(hours=0) < tiempo_restante <= timedelta(days=1):
            send_mail(
                subject='📦 Recordatorio de retiro de medicamento',
                message=mensaje,
                from_email='arteagamendozadiegodev@gmail.com',
                recipient_list=[usuario['correo']],
                fail_silently=False
            )

