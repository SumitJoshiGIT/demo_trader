import click

def validate_positive_float(ctx, param, value):
    if value is not None and value <= 0:
        raise click.BadParameter(f"{param.name} must be a positive number.")
    return value

def validate_symbol(ctx, param, value):
    if not value.isalnum():
        raise click.BadParameter("Symbol must be alphanumeric.")
    return value.upper()

def validate_side(ctx, param, value):
    value = value.upper()
    if value not in ['BUY', 'SELL']:
        raise click.BadParameter("Side must be either BUY or SELL.")
    return value

def validate_order_type(ctx, param, value):
    value = value.upper()
    if value not in ['MARKET', 'LIMIT', 'STOP_MARKET']:
        raise click.BadParameter("Order type must be MARKET, LIMIT, or STOP_MARKET.")
    return value
