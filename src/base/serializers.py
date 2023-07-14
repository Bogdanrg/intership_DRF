class ActionSerializerMixin:
    serializer_classes_by_action = None

    def get_serializer_class(self):
        try:
            return self.serializer_classes_by_action[self.action]

        except Exception:
            return self.serializer_class
