def get_model(self, model):
    if isinstance(model, str):
        return self._decl_class_registry[model]
    else:
        return model