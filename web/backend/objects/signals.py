from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    ObjectTerritory, EntranceGroup, MovementWays, 
    ServiceZones, SanitaryRooms, InfoTelecom, 
    ObjectAccessibilityResult
)

def save_res(obj, sec, k, o, z, s):
    ObjectAccessibilityResult.objects.update_or_create(
        object=obj, section=sec,
        defaults={'k_status': k, 'o_status': o, 'z_status': z, 's_status': s}
    )

@receiver(post_save, sender=ObjectTerritory)
def c_terr(sender, instance, **kw):
    k = 'accessible' if instance.entrance_width_ok else 'not_accessible'
    save_res(instance.object, 'territory', k, 'accessible', 'accessible', 'accessible')

@receiver(post_save, sender=EntranceGroup)
def c_ent(sender, instance, **kw):
    k = 'accessible' if instance.has_ramp else 'not_accessible'
    z = 'accessible' if instance.has_braille else 'not_accessible'
    save_res(instance.object, 'entrance', k, k, z, 'accessible')

@receiver(post_save, sender=MovementWays)
def c_mov(sender, instance, **kw):
    save_res(instance.object, 'movement', 'partial', 'partial', 'partial', 'accessible')

@receiver(post_save, sender=ServiceZones)
def c_ser(sender, instance, **kw):
    save_res(instance.object, 'service', 'accessible', 'accessible', 'accessible', 'accessible')

@receiver(post_save, sender=SanitaryRooms)
def c_san(sender, instance, **kw):
    k = 'accessible' if instance.toilet_accessible else 'not_accessible'
    save_res(instance.object, 'sanitary', k, 'accessible', 'accessible', 'accessible')

@receiver(post_save, sender=InfoTelecom)
def c_inf(sender, instance, **kw):
    save_res(instance.object, 'info', 'accessible', 'accessible', 'accessible', 'accessible')