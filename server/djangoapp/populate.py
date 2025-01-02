from .models import CarMake, CarModel, Dealer

def initiate():
    # Create car makes
    car_make_data = [
        {"name":"NISSAN", "description":"Great cars. Japanese technology"},
        {"name":"Mercedes", "description":"Great cars. German technology"},
        {"name":"Audi", "description":"Great cars. German technology"},
        {"name":"Kia", "description":"Great cars. Korean technology"},
        {"name":"Toyota", "description":"Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(CarMake.objects.create(name=data['name'], description=data['description']))

    # Assuming Dealer model exists and has been populated
    dealer_instances = Dealer.objects.all()  # Fetch all dealer instances

    # Create car models and link them to car makes and dealers
    car_model_data = [
        {"name":"Pathfinder", "type":"SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": dealer_instances[0]},
        {"name":"Qashqai", "type":"SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": dealer_instances[1]},
        {"name":"XTRAIL", "type":"SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": dealer_instances[2]},
        {"name":"A-Class", "type":"SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": dealer_instances[2]},
        {"name":"C-Class", "type":"SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": dealer_instances[3]},
        {"name":"E-Class", "type":"SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": dealer_instances[3]},
        {"name":"A4", "type":"SUV", "year": 2023, "car_make": car_make_instances[2], "dealer_id": dealer_instances[4]},
        {"name":"A5", "type":"SUV", "year": 2023, "car_make": car_make_instances[2], "dealer_id": dealer_instances[4]},
        {"name":"A6", "type":"SUV", "year": 2023, "car_make": car_make_instances[2], "dealer_id": dealer_instances[5]},
        {"name":"Sorrento", "type":"SUV", "year": 2023, "car_make": car_make_instances[3], "dealer_id": dealer_instances[5]},
        {"name":"Carnival", "type":"SUV", "year": 2023, "car_make": car_make_instances[3], "dealer_id": dealer_instances[6]},
        {"name":"Cerato", "type":"Sedan", "year": 2023, "car_make": car_make_instances[3], "dealer_id": dealer_instances[6]},
        {"name":"Corolla", "type":"Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": dealer_instances[7]},
        {"name":"Camry", "type":"Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": dealer_instances[7]},
        {"name":"Kluger", "type":"SUV", "year": 2023, "car_make": car_make_instances[4], "dealer_id": dealer_instances[8]},
        # Add more CarModel instances as needed
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            car_make=data['car_make'],
            type=data['type'],
            year=data['year'],
            dealer_id=data['dealer_id']
        )
