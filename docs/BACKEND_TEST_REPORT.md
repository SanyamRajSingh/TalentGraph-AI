# Phase 2: Backend Verification
Status: PASSED
Execution Time: 31.19s

## Output
```
ycopg2 PASSED [100%]

============================== warnings summary ===============================
..\..\..\anaconda3\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\sanya\anaconda3\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

..\..\..\anaconda3\Lib\site-packages\pythonjsonlogger\jsonlogger.py:11
  C:\Users\sanya\anaconda3\Lib\site-packages\pythonjsonlogger\jsonlogger.py:11: DeprecationWarning: pythonjsonlogger.jsonlogger has been moved to pythonjsonlogger.json
    warnings.warn(

tests/candidate/test_batch_api.py::test_batch_upload_zip
  <string>:8: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).

tests/candidate/test_batch_api.py::test_batch_upload_zip
  C:\Users\sanya\OneDrive\Documents\TalentGraph AI\apps\api\app\pipelines\batch_pipeline.py:90: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    job.completed_at = datetime.utcnow()

..\..\..\anaconda3\Lib\site-packages\_pytest\cacheprovider.py:475
  C:\Users\sanya\anaconda3\Lib\site-packages\_pytest\cacheprovider.py:475: PytestCacheWarning: cache could not write path C:\Users\sanya\OneDrive\Documents\TalentGraph AI\apps\api\.pytest_cache\v\cache\nodeids: [Errno 13] Permission denied: 'C:\\Users\\sanya\\OneDrive\\Documents\\TalentGraph AI\\apps\\api\\.pytest_cache\\v\\cache\\nodeids'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================= 87 passed, 5 warnings in 27.08s =======================
 # Truncated
```
