from flask import abort

def validate_motor_data(data):

    #  Validates the motor data provided by the client.
    
    # Args:
    #     data (dict): The data to validate.

    # Raises:
    #     Exception: If data is invalid or missing required fields.
    
    # Required Fields:
    #     - name: str, name of the motor.
    #     - type: str, type/category of the motor.
    #     - power: int, power rating of the motor.


    required_fields = ['name', 'type', 'power']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing required field: {field}")
            if not isinstance(data['power'], (int, float)):
                abort(400, description="Power must be a number")
                if not isinstance(data['power'], int):
                    abort(400, description="Power must be a number")
                if not isinstance(data['type'], str):
                    abort(400, description="Type must be a string")
