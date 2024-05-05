# Summary 
This is a summary about the steps done to solve the assessment: Fix the three failing tests.

## test_multi_update
    - Issue: Method `PATCH` is not allowed.
    - Solution:
        - Root cause: URL settings are not allowing `PATCH`, even though the router
                      inherits from DefaultRouter that contains the `UpdateModelMixin`
                      and provides default `partial_update()` action.
        - Actions:
            - First approach (failed):
                - Add `PATCH` to the `api/views.py` file by overriding the property
                  `allowed_methods`.
                - Override the `partial_update` method to handle the data update.
            - Second approach (failed):
                - Add a serializer `QuestionUpdateSerializer` in the `api\serializers.py`
                  file.
                - Override the `update` method to handle the data update.
                - Override the `get_serializer_class` method in the `api\views.py`
                  to return the new serializer class based on the HTTP method.				
            - Thrid approach (passed):
                - Add a custom router to handle the `List Route` from the `SimpleRouter`.
                - Override the `partial_update` method to handle the data update.
    - Complexity: Hard

## test_has_date_created
    - Issue: `date_created` is not in the data content.
    - Solution:
        - Root cause: The model `Question` in `poll/models.py` doesn't have a
                      `date_created` field.
        - Actions:
            - Add the new field to the `models.py`.
            - Add the new field also to its serializers file in `api/serializers.py`
              at the class `QuestionSerializer`.
            - Make migrations and apply it to update the schema db:
                - `python .\manage.py makemigrations polls`
                    - Used `option 1`: Provide a one-off default now which will be
                      set on all existing rows (timezone.now as per suggestion).
                - `python .\manage.py migrate`
    - Complexity: Easy

## test_query_count_is_off
    - Issue: Number of queries executed during a list request is higher than expected.
    - Solution:
        - Root cause: Django is getting the `polls_choice` objects individually
                      for each `polls_question` in the query list, increasing the
                      number of queries.
        - Actions: Optimize the queryset used to getting the list of questions to
                   retrieving the related `polls_choice`.
            - Options to use are:
                - `select_related`: It works well for `OneToOne` relationships, 
                                    however, it does not work with `ManyToMany`
                                    relationships.
                - `prefetch_related`: It works well for `OneToOne` and `ManyToMany`
                                      relationships.
            - As the `Question` model has a `OneToMany` relationship with the `Choice`
              model, `prefetch_related` is the better option here.
    - Complexity: Easy
