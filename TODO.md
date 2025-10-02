# TODO - Known Issues and Future Work

## 🚧 In Progress / Known Issues

### Custom Mesh Tab (Tab #6)
**Status:** Partially Functional - Needs Testing & Bug Fixes

**Known Issues:**
- [ ] STL file loading still has issues with some files
- [ ] Face normals computation may not work for all STL formats
- [ ] Need better error messages when mesh loading fails
- [ ] Camera positioning sometimes shows empty scene
- [ ] Scale defaults may not work well for all mesh sizes

**To Fix:**
- Add mesh bounding box detection for automatic camera positioning
- Implement mesh validation before rendering
- Add preview/wireframe mode
- Better default scale based on mesh dimensions
- Support for more file formats (FBX, COLLADA, glTF)
- Add mesh statistics display (vertices, faces, etc.)

**Test Cases Needed:**
- [ ] Test with various OBJ files
- [ ] Test with various PLY files (ASCII and binary)
- [ ] Test with various STL files (ASCII and binary)
- [ ] Test with very large meshes (100k+ vertices)
- [ ] Test with very small meshes
- [ ] Test with multi-material meshes

---

### Inverse Rendering Tab (Tab #7)
**Status:** Informational Only - Interactive Features Not Implemented

**Current State:**
- ✅ Variant checker works
- ✅ Documentation links provided
- ✅ Example runner instructions
- ❌ No interactive rendering
- ❌ No optimization visualization
- ❌ No parameter recovery interface

**Missing Features:**
- [ ] Interactive image upload for target
- [ ] Real-time optimization progress display
- [ ] Loss curve plotting
- [ ] Parameter sliders for optimization targets
- [ ] Preview during optimization iterations
- [ ] Export recovered parameters to file
- [ ] Multi-image reconstruction interface
- [ ] NeRF-style GUI integration

**Dependencies:**
- Requires AD variant (llvm_ad_rgb or cuda_ad_rgb)
- Needs matplotlib for plotting
- May need additional optimization libraries

**Implementation Plan:**
1. Create optimization worker thread (similar to render worker)
2. Add image upload widget
3. Implement loss visualization
4. Add optimization parameter controls
5. Create results export functionality

---

## 🎯 High Priority TODOs

### GUI Stability
- [ ] Fix graceful shutdown issues (QProcess cleanup)
- [ ] Add proper error handling for mesh loading failures
- [ ] Implement rendering timeout (prevent infinite hangs)
- [ ] Add cancellation for long-running operations
- [ ] Better logging for debugging

### Custom Mesh Improvements
- [ ] Auto-detect mesh scale and position camera appropriately
- [ ] Add mesh info display (vertex count, bounds, etc.)
- [ ] Support texture maps (diffuse, normal, roughness)
- [ ] Add material presets library
- [ ] Implement mesh transform preview (before render)

### Inverse Rendering Implementation
- [ ] Build interactive optimization interface
- [ ] Add target image upload
- [ ] Implement gradient descent visualization
- [ ] Create parameter recovery UI
- [ ] Add optimization presets (albedo, position, lighting)

### Documentation
- [x] Create GUI_NEW_FEATURES.md
- [ ] Add troubleshooting guide for mesh loading
- [ ] Create video tutorial for custom mesh workflow
- [ ] Document inverse rendering examples in detail
- [ ] Add FAQ section

### Testing
- [ ] Create unit tests for mesh loading
- [ ] Test with various file formats
- [ ] Performance testing with large meshes
- [ ] Cross-platform testing (Windows/Linux/macOS)
- [ ] Add automated GUI tests

---

## 🔮 Future Enhancements

### Advanced Features
- [ ] Animation timeline for keyframe animation
- [ ] Material library browser with previews
- [ ] HDRI environment map browser
- [ ] Batch rendering queue
- [ ] Cloud rendering integration
- [ ] Real-time preview mode (lower quality, faster)

### Custom Mesh Advanced
- [ ] Mesh editing capabilities (basic transforms)
- [ ] Instance rendering (multiple copies)
- [ ] Procedural mesh generation
- [ ] Mesh simplification/decimation
- [ ] Normal map baking
- [ ] UV unwrapping visualization

### Inverse Rendering Advanced
- [ ] Multi-view reconstruction
- [ ] NeRF integration (Neural Radiance Fields)
- [ ] Photogrammetry pipeline
- [ ] BRDF estimation from photos
- [ ] Light stage capture processing
- [ ] Appearance modeling from images

### User Experience
- [ ] Dark/Light theme toggle
- [ ] Customizable keyboard shortcuts
- [ ] Preset saving/loading system
- [ ] Recent files menu
- [ ] Drag-and-drop file loading
- [ ] Render history browser

### Performance
- [ ] Multi-threaded mesh loading
- [ ] Progressive rendering preview
- [ ] GPU acceleration options
- [ ] Render queue with priority
- [ ] Distributed rendering support

---

## 🐛 Bug Tracker

### Critical Bugs
- **GUI Close Error**: QProcess cleanup may still have issues
  - Location: `gui/core/main_window.py` closeEvent()
  - Impact: Prevents graceful shutdown
  - Priority: HIGH

### Major Bugs  
- **STL Loading Failure**: Some STL files fail with normals error
  - Location: `gui_examples/custom_mesh.py`
  - Error: "Storing new normals in a Mesh that didn't have normals at construction time"
  - Workaround: Added face_normals flag, but not working for all files
  - Priority: HIGH

### Minor Bugs
- **LLVM Warning Spam**: LLVM initialization warnings clutter console
  - Location: Mitsuba core (external)
  - Impact: Cosmetic only
  - Priority: LOW

---

## 📋 Code Quality TODOs

### Refactoring Needed
- [ ] Extract common parameter widgets to reusable components
- [ ] Consolidate material creation logic
- [ ] Create mesh loader utility class
- [ ] Separate GUI logic from scene generation
- [ ] Add type hints throughout codebase

### Code Review Items
- [ ] Review error handling patterns
- [ ] Check for memory leaks in QProcess handling
- [ ] Validate all user inputs properly
- [ ] Add docstrings to all public methods
- [ ] Remove debug print statements

### Technical Debt
- [ ] Replace pickle-based IPC with JSON or protobuf
- [ ] Implement proper logging levels
- [ ] Add configuration file support
- [ ] Create plugin system for custom tabs
- [ ] Migrate to PyQt6 best practices

---

## 🎓 Learning Resources to Create

- [ ] "Getting Started with Custom Meshes" tutorial
- [ ] "Understanding Inverse Rendering" guide
- [ ] "Material System Deep Dive" article
- [ ] "Optimization Techniques in Mitsuba 3" guide
- [ ] Video: "Custom Mesh Workflow Walkthrough"
- [ ] Video: "Inverse Rendering Examples Explained"

---

## 📊 Metrics to Track

- [ ] Average render time per scene type
- [ ] Most used features (telemetry opt-in)
- [ ] Common error patterns
- [ ] User workflow patterns
- [ ] Performance benchmarks

---

## 🚀 Release Checklist (Before v1.2.0)

### Must Have
- [ ] Fix critical bugs (GUI close, STL loading)
- [ ] Test all 7 tabs on fresh install
- [ ] Update all documentation
- [ ] Create release notes
- [ ] Test on Windows/Linux/macOS

### Should Have
- [ ] Working custom mesh tab for OBJ/PLY files
- [ ] Inverse rendering examples runnable
- [ ] Comprehensive error messages
- [ ] User guide/tutorial

### Nice to Have
- [ ] Interactive inverse rendering demo
- [ ] Video tutorials
- [ ] Community examples gallery
- [ ] Performance optimizations

---

## 📝 Notes

**Last Updated:** October 3, 2025

**Current Version:** 1.1.0 (dev)  
**Target Version:** 1.2.0 (with stable custom mesh + inverse rendering info)

**Contributors Welcome!**
These TODOs are tracked for community contributions. Feel free to pick any item and submit a PR!

**Priority Legend:**
- 🔴 HIGH - Critical bugs, blocking issues
- 🟡 MEDIUM - Important features, usability improvements  
- 🟢 LOW - Nice to have, polish, future enhancements

---

## Contact & Support

For questions about these TODOs or to contribute:
- Check existing GitHub issues
- Create new issue with [TODO] prefix
- Reference this file in discussions
- Join community Discord (if available)
