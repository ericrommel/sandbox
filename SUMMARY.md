# Summary 
This is a summary about the steps done to solve the assessment: Fix the three failing tests.

## test_multi_update

## test_has_date_created
    - Issue: `date_created` is not in the data content.
    - Solution:
        - Root cause: The model `Question` in `poll/models.py` doesn't have a `date_created` field.
        - Actions:
            - Add the new field to the `models.py`.
            - Add the new field also to its serializers file in `api/serializers.py` at the class `QuestionSerializer`.
            - Make migrations and apply it to update the schema db:
                - `python .\manage.py makemigrations polls`
                    - Used `option 1`: Provide a one-off default now which will be set on all existing rows (timezone.now as per suggestion).
                - `python .\manage.py migrate`

## test_query_count_is_off
