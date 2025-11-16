from .time_slot_manager import TimeSlotManager

# Initialize with database path
_time_slot_manager = TimeSlotManager('transport.db')

def get_available_time_slots():
    """Get available time slots for booking"""
    settings = _time_slot_manager.get_global_settings()
    if settings and settings['enabled']:
        return f"{settings['start_time']} - {settings['end_time']}"
    return "All hours available"

def validate_booking_time(booking_time_str):
    """Validate booking time against time slot restrictions"""
    return _time_slot_manager.validate_booking_time(booking_time_str)

def get_campaign_time_slots():
    """Get all campaign time slots"""
    return _time_slot_manager.get_campaign_slots()
