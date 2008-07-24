#!/bin/sh

./tools/bulkload_client.py --filename data/shop_converted.csv --kind Shop --url http://localhost:8080/admin/load/shop --cookie='dev_appserver_login="test@example.com:True"'

#./tools/bulkload_client.py --filename /path/to/file.csv --kind Area --url http://beta.chin-ma-ya.org/update/area --cookie='ACSID=AJKiYcGKdMn1MB99cJU4kZGB-Va2uBkptotVCpTdxt6LOeijc7eu3JKF-m7pltoPSK3gA7G3P5dquMgqmWkcj0sbkY4_vHNNAeWyKHvKyQCpZ8UkyNtXM5-UUe2YjC0S6BXeeuB2BB16LeOPRh0hPdYjZuwBF2E-dqn3CRRivCZLJxIdjOnr3lm1Kh9_b-7_tvwdC9yD3tqtdl-IEAsZwoi4kBRcKrYze71XcJHf-8EKuG_-HOXKWCFNGONShG6DoAdZfLJRZxJ-WUoSCmxaGOKGLDCDvwll6X-IU0_1yyLyEGG3QxK56DXTxrn2gmvaDdAadYx8KgvHa383RD3T7SZxTlH4bp9YFM2GnQQTfxf2xEq4oLHbfuuiuqGezOQU5ThzyHXoyc7WQj56DDjs7vSaQUa2KWsjqCTiR7coe_YJRmoS6_ZIPUY'

