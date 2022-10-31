# 3 Abstração
class SerializerByMethodMixin:

    serializer_map = None

    def get_serializer_class(self):
        assert (
            self.serializer_map is not None
        ), f"'{self.__class__.__name__}' should include a `serializer_map` attribute"

        return self.serializer_map.get(self.request.method)
