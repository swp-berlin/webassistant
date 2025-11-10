from typing import List

from drf_spectacular.openapi import AutoSchema

from .viewsets import SWPViewSet


class SWPSchema(AutoSchema):

    def is_excluded(self) -> bool:
        return 'v1' not in self.path

    def _tokenize_path(self) -> List[str]:
        """
        Remove the v1 prefix from tokenized path.
        """

        prefix, *tokenized_path = AutoSchema._tokenize_path(self)

        return tokenized_path

    def get_operation_id(self) -> str:
        operation_id = AutoSchema.get_operation_id(self)

        if isinstance(self.view, SWPViewSet):
            if self.view.action not in self.method_mapping.values():
                action = self.method_mapping[self.method.lower()]

                return operation_id.removesuffix(f'_{action}')

        return operation_id

    def get_summary(self) -> str:
        return self.path
