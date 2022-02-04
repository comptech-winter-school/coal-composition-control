#!/bin/bash

cd vision_document && markdown-enum vision_document.md 1 vision_numbered.md && cd ..
cd users_guide && markdown-enum users_guide.md 1 users_numbered.md && cd ..
