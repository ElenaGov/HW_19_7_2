from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# Тесты для GET api/key

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result =pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result 

def test_get_api_key_for_invalid_user(email='invalid_email@mail.ru', password=valid_password):
    status, result =pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_password(email=valid_email, password='invalid_password'):
    status, result =pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    
# Тесты для GET api/pets

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(filter=''):
    auth_key = {
        "key": "TEST"
    }
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'pets' not in result

# Тесты для POST api/pets

def test_successful_add_new_pet(name='ESG_cat', animal_type='Siberian', age='3', pet_photo='images/esg_cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name 

def test_add_new_pet_with_empty_name(name='', animal_type='Siberian', age='33', pet_photo='images/esg_cat2.jpg'):
# Запрос добавляет питомца без name - БАГ api!
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert 'name' not in result

def test_add_new_pet_with_empty_animal_type(name='Busa', animal_type='', age='33', pet_photo='images/esg_cat2.jpg'):
# Запрос добавляет питомца без animal_type - БАГ api!
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert 'animal_type' not in result

def test_add_new_pet_with_empty_age(name='Busa', animal_type='dog', age='', pet_photo='images/esg_cat2.jpg'):
# Запрос добавляет питомца без age - БАГ api!
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert 'age' not in result

def test_add_new_pet_with_age_is_string(name='Busa', animal_type='dog', age='TEST', pet_photo='images/esg_cat2.jpg'):
# Запрос добавляет питомца с нечисловым age - БАГ api!
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert 'age' not in result

# Тесты для DELETE api/pets/{pet_id}

def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_information_about_new_pet(auth_key, "ESG_cat_for_deleting", "cat", "1", "images/esg_cat2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_pet_with_invalid_auth_key():
# Можно удалить в Swagger с неправильным auth_key - БАГ в Swagger!
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_information_about_new_pet(auth_key, "ESG_cat_for_deleting", "cat", "1", "images/esg_cat2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet = my_pets['pets'][0]['id']
    new_key = {
        "key": "TEST"
    }
    status, _ = pf.delete_pet(auth_key=new_key, pet_id=pet)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 403
    assert pet == my_pets['pets'][0]['id']

# Тесты для PUT api/pets/{pet_id}

def test_successful_update_self_pet_info(name='ESG_UPDATE_NAME', animal_type='CAT', age=22):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# Тесты для POST /api/create_pet_simple

def test_successful_add_new_pet_without_photo(name='ESG_cat_without_photo', animal_type='Himalayan', age='12'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['pet_photo'] == ""

# Тесты для POST /api/pets/set_photo/{pet_id}

def test_successful_add_photo_to_pet(pet_photo="images/no_photo.jpg"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_to_existing_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
       raise Exception("There is no my pets")

def test_add_unselected_photo(pet_photo=""):
# Неуказан файл для pet_photo-это обязательный параметр, ожидаю код 400 как случай неправильных данных, получаю эксепшин - БАГ api (уточнить у аналитика)!
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_information_about_new_pet_without_photo(auth_key, name='Animal Test name', animal_type='test type', age=3)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_photo_to_existing_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    assert status == 400

def test_add_photo_with_format_tif(pet_photo="images/BadImageFormat.tif"):
# Добавление фото с форматом несоответствующим описанным в документации Swagger (JPG,JPEG ,PNG) - БАГ api (Swagger тоже позволяет добавлять такое фото, уточнить у аналитика)!
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result1 = pf.add_information_about_new_pet_without_photo(auth_key, name='Animal without photo', animal_type='test type', age=3)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_photo_to_existing_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    assert status == 400
    assert result['pet_photo'] == result1['pet_photo']