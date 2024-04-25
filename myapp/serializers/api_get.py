# serializers.py
from rest_framework import serializers
from myapp.models import Restaurante, Imagen, Plato, Ingrediente


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id', 'nombre']

class PlatoSerializer(serializers.ModelSerializer):
    ingredientes = IngredienteSerializer(many=True, read_only=True)

    class Meta:
        model = Plato
        fields = ['id', 'nombre', 'precio', 'descuento', 'ingredientes']

class ImagenSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Imagen
        fields = ['id', 'imagen_url']

    def get_imagen_url(self, imagen):
        # Aquí asumimos que la imagen está almacenada en el directorio 'imagenes_restaurante'
        # en el servidor.
        return imagen.imagen.url

class RestauranteSerializer(serializers.ModelSerializer):
    imagens = ImagenSerializer(many=True, read_only=True)
    direccion_completa = serializers.SerializerMethodField()
    cordenadas = serializers.SerializerMethodField()

    class Meta:
        model = Restaurante
        fields = ['id', "nombre", "descripcion", "negocio", "imagens", 'direccion_completa', 'cordenadas']

    def get_direccion_completa(self, restaurante):
        return restaurante.ubicacion.full_address()

    def get_cordenadas(self, restaurante):
        return {
            'latitud': restaurante.ubicacion.latitud,
            'longitud': restaurante.ubicacion.longitud
        }



