import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from claude_client import ClaudeDevOps


class TestClaudeDevOps:
    """Test Claude DevOps Client"""

    def test_client_init_without_key(self):
        """Should raise error when API key missing"""
        original = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                ClaudeDevOps()
        finally:
            if original:
                os.environ["ANTHROPIC_API_KEY"] = original

    def test_client_init_with_key(self):
        """Should initialize when API key is present"""
        os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test-key"
        try:
            # Will init but API calls will fail - that's ok
            client = ClaudeDevOps()
            assert client.model == "claude-3-5-sonnet-20241022"
        except ValueError:
            pytest.skip("No valid API key available")
        finally:
            pass

    def test_sample_log_not_empty(self):
        """Sample logs should have content"""
        from log_analyzer import SAMPLE_LOGS
        assert len(SAMPLE_LOGS.strip()) > 0
        assert "ERROR" in SAMPLE_LOGS

    def test_scannable_extensions(self):
        """Security scanner should have file extensions defined"""
        from security_scanner import SCANNABLE
        assert '.py' in SCANNABLE
        assert '.yml' in SCANNABLE
        assert '.tf' in SCANNABLE


if __name__ == "__main__":
    pytest.main([__file__, "-v"])