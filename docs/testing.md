# Testing


## Testing Tools

- **Django Test Framework**: The built-in Django test framework is used for writing and running tests. It provides tools
  for creating test cases, assertions, and test runners.
- **Coverage.py**: This tool measures code coverage, indicating which parts of the codebase are tested and which are
  not.
- **Mock**: The `unittest.mock` module is used to replace parts of the system under test and make assertions about how
  they have been used.

## Running Tests

To run the tests, use the following command:

```bash
python manage.py test
```

This command will discover and execute all test cases in the application.

## Code Coverage

To measure code coverage, use the following command:

```bash
coverage run manage.py test
coverage report
```

This will generate a coverage report showing the percentage of code covered by tests.

## Functionality Covered by Tests

The current test suite covers a wide range of functionalities within the SWP application, including:

- **Scraping Functionality**: Tests in `swp/scraper/tests.py` cover the configuration and execution of web scrapers,
  ensuring that data is correctly extracted from specified sources.
- **API Endpoints**: Tests in `swp/api/tests/` cover various API endpoints, including:
    - **Monitor API**: Tests for creating, listing, and retrieving monitor details.
    - **Thinktank API**: Tests for listing, filtering, and managing thinktank data.
    - **Publication API**: Tests for listing, filtering, and retrieving publication details.
    - **Publication List API**: Tests for managing publication lists, including adding and removing publications.
- **Authentication and User Management**: Tests in `swp/views/tests.py` cover authentication workflows, such as login
  and password reset, as well as user data retrieval and permission checks.
- **Admin Interface**: Tests in `swp/admin/tests.py` ensure that the admin interface is correctly configured and
  accessible for various models.




