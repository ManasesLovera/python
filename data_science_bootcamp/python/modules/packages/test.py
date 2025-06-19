from typing import List, Dict, Callable, Any

def test_function(
        func: Callable[..., Any], 
        test_cases: List[Dict[str, Any]]
        ) -> None:

    failed_values: List = []
    for case in test_cases:
        expected_result = case['expected_result']
        test_case = case['test_case']
        result = None
        try:
            # ❌ Reject dicts explicitly
            if isinstance(test_case, dict):
                raise TypeError("Dicts are not allowed as test case values.")
            
            # Unpack tuple or set
            if isinstance(test_case, (tuple, set)):
                result = func(*test_case)
            else:
                result = func(test_case)
            assert result == expected_result

        except AssertionError:
            print(f"❌ Test failed for case: {test_case}")
            print(f"Expected: {expected_result}, but got: {result}")
            failed_values.append(case)
        except TypeError as e:
            print(f"❌ Type error for case: {test_case}")
            print(f"Error message: {e}")
            failed_values.append(case)
        except Exception as e:
            print(f"An error occurred: {e}")
            failed_values.append(case)

    if not failed_values:
        print("✅ All tests passed!")