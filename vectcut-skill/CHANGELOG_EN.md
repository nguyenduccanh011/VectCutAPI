# Changelog

This document records all important changes in the VectCutAPI Skill project.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2025-01-25

### Added

#### Core Features
- Complete VectCutAPI Skill wrapper
- Python client library `vectcut_client.py`
- Support for 35+ HTTP API endpoints
- Support for 11 MCP tools

#### Documentation
- SKILL.md main documentation (11KB)
- API reference documentation `api_reference.md` (13KB)
- Workflow examples `workflows.md` (17KB)
- Technical architecture documentation `ARCHITECTURE.md`
- Usage guide `USAGE.md`
- Installation guide `INSTALLATION.md`
- English and Chinese README

#### Python Client Features
- VectCutClient core class
- Preset enum types (Resolution, Transition, TextAnimation)
- Data classes (DraftInfo, ApiResult)
- Context manager support
- Complete error handling

#### Workflow Examples
- Basic video production
- AI text-to-video
- Video mashup
- Video with subtitles
- Keyframe animation
- Product intro video
- Split screen effect
- Image slideshow

#### Project Configuration
- MIT License
- .gitignore configuration
- Complete project directory structure

---

## [Future Plans]

### v1.1.0 (Planned)
- [ ] Add unit tests
- [ ] Add CLI tools
- [ ] Support async requests
- [ ] Add more preset values

### v1.2.0 (Planned)
- [ ] Web UI interface
- [ ] Configuration file support
- [ ] Plugin system
- [ ] Cloud deployment solutions

---

## Release Notes

### Version Format

- **Major version**: Breaking API changes
- **Minor version**: Backward-compatible feature additions
- **Patch version**: Backward-compatible bug fixes

### Change Types

- **Added** - New features
- **Changed** - Feature changes
- **Deprecated** - Features to be removed
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security-related fixes

---

## Acknowledgments

Thanks to the following projects for their support:

- [VectCutAPI](https://github.com/sun-guannan/VectCutAPI) - Core video editing API
- [Claude Code](https://claude.com/claude-code) - Anthropic official CLI tool
- [Anthropic](https://www.anthropic.com) - AI technology support

---

[1.0.0]: https://github.com/your-username/vectcut-skill/releases/tag/v1.0.0
